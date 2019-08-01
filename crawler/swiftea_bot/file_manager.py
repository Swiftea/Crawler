#!/usr/bin/env python3

"""Swiftea-Crawler use a lot of files. For example to config the app, save links...
Here is a class that manage files of crawler.
"""

from os import path, remove, listdir, mkdir, rename
from configparser import ConfigParser
import json
from zipfile import ZipFile


from crawler.swiftea_bot import data
from crawler.swiftea_bot.module import tell, remove_duplicates, convert_keys, safe_quit
import crawler.swiftea_bot.links as swiftea_bot_links


class FileManager(object):
	"""File manager for Swiftea-Crawler.

	Save and read links, read and write configuration variables,
	read inverted-index from json saved file and from used file when sending it.

	Create configuration file if it doesn't exists or read it.

	"""
	def __init__(self, crawl_option=None):
		"""With `url`, filter links to save, and read filtered links.

		:param url: the crawler was called with this starting url
		:type url: str

		"""
		self.crawl_option = crawl_option if crawl_option else {
			'domain': '',
			'level': -1,
			'target-level': -1
		}
		self.max_links = data.MAX_LINKS  # Number of maximum links in a file
		self.run = 'true'  # Run program bool
		self.config = ConfigParser()
		self.domains = []  # in FILE_LINKS

		if not path.exists(data.FILE_CONFIG):
			# Create the config file:
			self.config['DEFAULT'] = {
				'run': 'true',
				'max_links': data.MAX_LINKS
			}

			with open(data.FILE_CONFIG, 'w') as configfile:
				self.config.write(configfile)
		else:
			# Read the config file:
			self.config.read_file(open(data.FILE_CONFIG))
			self.run = self.config['DEFAULT']['run']
			self.max_links = int(self.config['DEFAULT']['max_links'])

	def check_stop_crawling(self):
		"""Check if the user wants to stop program."""
		self.config.read_file(open(data.FILE_CONFIG))
		self.run = self.config['DEFAULT']['run']

	def save_config(self):
		"""Save all configurations in config file."""
		self.config['DEFAULT'] = {
			'run': self.run,
			'max_links': str(self.max_links)
		}
		with open(data.FILE_CONFIG, 'w') as configfile:
			self.config.write(configfile)

	def save_links(self, links):
		"""Save found links in file.

		Save links in a file without doublons.

		:param links: links to save
		:type links: list

		:return: True is the level is completed

		"""
		self.domains = swiftea_bot_links.save_links(
			links,
			self.crawl_option,
			self.max_links
		)

	def check_size_files(self):
		for filelog in [data.FILE_EVENTS, data.FILE_ERRORS]:
			filearchive = filelog[:-3] + 'zip'
			if not path.exists(filelog):
				continue
			with open(filelog, 'r') as myfile:
				content = myfile.readlines()
			if len(content) > data.MAX_SIZE:
				if not path.exists(filearchive):
					ZipFile(file=filearchive, mode='w').close()
					filename = '0'
				else:
					with ZipFile(filearchive, 'r') as myzip:
						filename = str(int(myzip.namelist()[-1])+1)  # The last one +1
				rename(filelog, filename)
				with ZipFile(filearchive, 'a') as myzip:
					myzip.write(filename)
				remove(filename)
				tell('Archiving ' + filelog + ': ' + filename, severity=-1)

	def get_url(self):
		url = self.read_links()
		if url == '#level_complete#':
			tell('Level complete, new level: ' + str(self.crawl_option['level']))
			self.crawl_option['level'] += 1
			swiftea_bot_links.save_domains(self.domains)
			if (self.crawl_option['level'] < self.crawl_option['target-level']):
				return self.read_links(), True
			else:
				return '#target-reached#', True
		return url, False

	def read_links(self):
		"""Get url of next webpage.

		Check the size of curent reading links and increment it if over.

		:return: url of webpage to crawl

		"""
		self.domains = swiftea_bot_links.get_domains()

		filename_ptr, reading_line_number = swiftea_bot_links.get_filename_read(
			self.domains,
			self.crawl_option
		)

		filename = data.DIR_LINKS + str(filename_ptr)

		if path.exists(filename):
			with open(filename, 'r', errors='replace', encoding='utf8') as myfile:
				list_links = myfile.read().splitlines()  # List of urls
		else:
			tell('Reading file not found in get_url: ' + filename, 4)
			return 'error'

		# If it's the last links of the file:
		if len(list_links) == reading_line_number-1:
			self.domains[filename_ptr]['completed'] = 1
			return '#level_complete#'

		tell('File {0}, line {1}'.format(
			str(filename_ptr),
			str(reading_line_number)), severity=0)
		url = list_links[reading_line_number-1]

		return url

	def save_inverted_index(self, inverted_index):
		"""Save inverted-index in local.

		Save it in a json file when we can't send it.

		:param inverted_index: inverted-index
		:type inverted_index: dict

		"""
		tell('Save inverted-index in save file')
		with open(data.FILE_INDEX, 'w') as myfile:
			json.dump(inverted_index, myfile, ensure_ascii=False)

	def get_inverted_index(self):
		"""Get inverted-index in local.

		Called after a connection error. Read a json file that contains the inverted-index.
		Delete this file after reading it.

		:return: inverted-index

		"""
		tell('Get inverted-index from save file')
		with open(data.FILE_INDEX, 'r') as myfile:
			inverted_index = json.load(myfile)
		remove(data.FILE_INDEX)
		return convert_keys(inverted_index)

	def read_inverted_index(self):
		"""Get inverted-index in local.

		Called after sending inverted-index without error.
		Read all files created to send inverted-index.

		:return: inverted-index

		"""
		tell('Get inverted-index in local')
		inverted_index = dict()
		for language in listdir(data.DIR_INDEX):
			inverted_index[language] = dict()
			for first_letter in listdir(data.DIR_INDEX + language):
				inverted_index[language][first_letter] = dict()
				for filename in listdir(data.DIR_INDEX + language + '/' + first_letter):
					with open(data.DIR_INDEX + language + '/' + first_letter + '/' + filename, 'r', encoding='utf-8') as myfile:
						inverted_index[language][first_letter][filename[:-4]] = json.load(myfile)
		return convert_keys(inverted_index)

	def get_lists_words(self):
		"""Get lists words from data

		Check for dirs lists words, create them if they don't exist.

		:return: stopwords, badwords

		"""
		stopwords = dict()
		badwords = dict()
		if path.isdir('stopwords/'):
			for filename in listdir('stopwords/'):
				with open('stopwords/' + filename, 'r') as myfile:
					stopwords[filename[:2]] = myfile.read().split()
		else:
			mkdir('stopwords/')
		if path.isdir('badwords/'):
			for filename in listdir('badwords/'):
				with open('badwords/' + filename, 'r') as myfile:
					badwords[filename[:2]] = myfile.read().split()
		else:
			mkdir('badwords/')
		return stopwords, badwords

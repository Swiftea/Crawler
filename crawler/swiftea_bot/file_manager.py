#!/usr/bin/python3

"""Swiftea-Crawler use lot a files. For example to manage configurations, stuck links...
Here is a class who manager files of crawler.
"""

from os import path, remove, listdir
from configparser import ConfigParser
import json

from swiftea_bot.data import MAX_LINKS, FILE_CONFIG, DIR_LINKS, FILE_INDEX, DIR_INDEX
from swiftea_bot.module import tell, remove_duplicates, convert_keys

class FileManager(object):
	"""File manager for Swiftea-Crawler.

	Save and read links, read and write configuration variables,
	read inverted-index from json file saved and from file using when send it.

	Create configuration file if doesn't exists	or read it.

	"""
	def __init__(self):
		self.writing_file_number = 1  # Meter of the writing file
		self.reading_file_number = 0  # Meter of the reading file
		self.reading_line_number = 0  # Meter of links in the reading file
		self.max_links = MAX_LINKS  # Number of maximum links in a file
		self.run = 'true'  # Run program bool
		self.config = ConfigParser()

		if not path.exists(FILE_CONFIG):
			# Create the config file:
			self.config['DEFAULT'] = {
				'run': 'true',
				'reading_file_number': '0',
				'writing_file_number': '1',
				'reading_line_number': '0',
				'max_links': MAX_LINKS
			}

			with open(FILE_CONFIG, 'w') as configfile:
				self.config.write(configfile)
		else:
			# Read the config file:
			self.config.read_file(open(FILE_CONFIG))
			self.run = self.config['DEFAULT']['run']
			self.reading_file_number = int(self.config['DEFAULT']['reading_file_number'])
			self.writing_file_number = int(self.config['DEFAULT']['writing_file_number'])
			self.reading_line_number = int(self.config['DEFAULT']['reading_line_number'])
			self.max_links = int(self.config['DEFAULT']['max_links'])

	def check_stop_crawling(self):
		"""Check if the user want to stop program."""
		self.config.read_file(open(FILE_CONFIG))
		self.run = self.config['DEFAULT']['run']

	def get_max_links(self):
		"""Get back the maximal number of links in a file from configuration file."""
		self.config.read_file(open(FILE_CONFIG))
		self.max_links = int(self.config['DEFAULT']['max_links'])

	def save_config(self):
		"""Save all configurations in config file."""
		self.config['DEFAULT'] = {
			'run': self.run,
			'reading_file_number': str(self.reading_file_number),
			'writing_file_number': str(self.writing_file_number),
			'reading_line_number': str(self.reading_line_number),
			'max_links': str(self.max_links)
		}
		with open(FILE_CONFIG, 'w') as configfile:
			self.config.write(configfile)


	def save_links(self, links):
		"""Save found links in file.

		Save link in a file without doublons and check if the file if full.

		:param links: links to save
		:type links: list

		"""
		filename = DIR_LINKS + str(self.writing_file_number)
		if not path.exists(filename):
			with open(filename, 'w', errors='replace', encoding='utf8') as myfile:
				myfile.write('\n'.join(links))
		else:
			with open(filename, 'r+', errors='replace', encoding='utf8') as myfile:
				old_links = myfile.read().splitlines()
				myfile.seek(0)
				links = remove_duplicates(old_links + links)
				myfile.write('\n'.join(links))

		return links

	def ckeck_size_links(self, links):
		"""Check number of links in file.

		:param links: links saved in file
		:type links: str

		"""
		if len(links) > self.max_links:  # Check the size
			self.writing_file_number += 1
			tell(
				'More than {0} links : {1} : writing file {2}.'.format(
				str(self.max_links), str(len(links)),
				str(self.writing_file_number)), severity=-1
			)


	def get_url(self):
		"""Get url of next webpage.

		Check the size of curent reading links and increment it if over.

		:return: url of webpage to crawl

		"""
		filename = DIR_LINKS + str(self.reading_file_number)
		try:
			with open(filename, 'r', errors='replace', encoding='utf8') as myfile:
				list_links = myfile.read().splitlines()  # List of urls
		except FileNotFoundError:
			tell('Reading file is not found in get_url: ' + filename, 4)
			return 'stop'
		else:
			url = list_links[self.reading_line_number]
			self.reading_line_number += 1
			# If is the last links of the file:
			if len(list_links) == (self.reading_line_number):
				self.reading_line_number = 0
				if self.reading_file_number != 0:  # Or > 0 ? wich is better ?
					remove(filename)
					tell('File ' + filename + ' removed', severity=-1)
				self.reading_file_number += 1
				# The program have read all the links: next reading_file_number
				tell('Next reading file: ' + str(self.reading_file_number), severity=-1)
			return url


	def save_inverted_index(self, inverted_index):
		"""Save inverted-index in local.

		Save it in a .json file when can't send.

		:param inverted_index: inverted-index
		:type inverted_index: dict

		"""
		tell('Save inverted-index in save file')
		with open(FILE_INDEX, 'w') as myfile:
			json.dump(inverted_index, myfile, ensure_ascii=False)

	def get_inverted_index(self):
		"""Get inverted-index in local.

		Call after a connxion error. Read a .json file conatin inverted-index.
		Delete this file after reading.

		:return: inverted-index

		"""
		tell('Get inverted-index form save file')
		with open(FILE_INDEX, 'r') as myfile:
			inverted_index = json.load(myfile)
		remove(FILE_INDEX)
		return convert_keys(inverted_index)

	def read_inverted_index(self):
		"""Get inverted-index in local.

		Call after sending inverted-index without error.
		Read all files created for sending inverted-index.

		:return: inverted-index

		"""
		tell('Get inverted-index in local')
		inverted_index = dict()
		for language in listdir(DIR_INDEX):
			inverted_index[language] = dict()
			for first_letter in listdir(DIR_INDEX + language):
				inverted_index[language][first_letter] = dict()
				for filename in listdir(DIR_INDEX + language + '/' + first_letter):
					with open(DIR_INDEX + language + '/' + first_letter + '/' + filename, 'r', encoding='utf-8') as myfile:
						inverted_index[language][first_letter][filename[:-4]] = json.load(myfile)
		return convert_keys(inverted_index)

#!/usr/bin/python3

"""Crawler use lot a files. For example to manage configurations, stuck links...
Here is a class who manager files of crawler."""

__author__ = "Seva Nathan"

from os import path, remove, listdir
from configparser import ConfigParser
import json


from package.data import MAX_LINKS, FILE_CONFIG, DIR_LINKS, FILE_INDEX, DIR_INDEX
from package.module import speak, stats_links, rebuild_links

class FileManager(object):
	"""File manager for crawler

	Save and read links, read and write configuration variables,
	read inverted-index and later archive event and errors files.

	"""
	def __init__(self):
		"""build manager

		Create configuration file if doesn't exists	or read it

		"""
		self.writing_file_number = 1 # meter of the writing file
		self.reading_file_number = 0 # meter of the reading file
		self.reading_line_number = 0 # meter of links in the reading file
		self.max_links = MAX_LINKS # number of maximum links in a file
		self.run = 'true' # run program bool
		self.config = ConfigParser()

		if not path.exists(FILE_CONFIG):
			# create the config file :
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
			# read the config file :
			self.config.read_file(open(FILE_CONFIG))
			self.run = self.config['DEFAULT']['run']
			self.reading_file_number = int(self.config['DEFAULT']['reading_file_number'])
			self.writing_file_number = int(self.config['DEFAULT']['writing_file_number'])
			self.reading_line_number = int(self.config['DEFAULT']['reading_line_number'])
			self.max_links = int(self.config['DEFAULT']['max_links'])

	# sometimes :

	def check_stop_crawling(self):
		"""Check if the user want to stop program"""
		self.config.read_file(open(FILE_CONFIG))
		self.run = self.config['DEFAULT']['run']

	def get_max_links(self):
		"""Get back the maximal number of links in a file from configuration file"""
		self.config.read_file(open(FILE_CONFIG))
		self.max_links = int(self.config['DEFAULT']['max_links'])

	def save_config(self):
		"""Save configurations"""
		self.config['DEFAULT'] = {
			'run': self.run,
			'reading_file_number': str(self.reading_file_number),
			'writing_file_number': str(self.writing_file_number),
			'reading_line_number': str(self.reading_line_number),
			'max_links': str(self.max_links)
		}
		with open(FILE_CONFIG, 'w') as configfile:
			self.config.write(configfile)

	# other :

	def save_links(self, links):
		"""Save links

		Save link in a file without doublons and check if the file if full

		:param links: links to save
		:type links: list

		"""
		stats_links(str(len(links)))
		filename = DIR_LINKS + str(self.writing_file_number)
		if not path.exists(filename):
			with open(filename, 'w', errors='replace', encoding='utf8') as myfile:
				myfile.write('\n'.join(links))
		else:
			with open(filename, 'r+', errors='replace', encoding='utf8') as myfile:
				old_links = myfile.read().split('\n')
				myfile.seek(0)
				links = rebuild_links(old_links, links)
				myfile.write(links)

		self.ckeck_size_links(links)

	def ckeck_size_links(self, links):
		"""Check number of links in file

		:param links: links saved in file
		:type links: str

		"""
		if len(links.split('\n')) > self.max_links: # check the size
			self.writing_file_number += 1
			speak(
				'More {0} links : {1} : writing file {2}.'.format(
				str(self.max_links), str(len(links)),
				str(self.writing_file_number))
			)

	def get_url(self):
		"""Get the url of the next webpage

		:return: url of webpage to crawl

		"""
		# joining : /liens/(reading meter) :
		filename = DIR_LINKS + str(self.reading_file_number)
		try:
			with open(filename, 'r', errors='replace',
				encoding='utf8') as myfile:
				list_links = myfile.read().splitlines() # list of urls
		except FileNotFoundError:
			# no link file
			speak('Reading file is not found in get_url : ' + filename, 4)
			return 'stop'
		else:
			url = list_links[self.reading_line_number]
			self.reading_line_number += 1
			# if is the last links of the file :
			if len(list_links) == (self.reading_line_number):
				self.reading_line_number = 0
				if self.reading_file_number != 0: # or > 0 ? wich is better ?
					remove(filename)
					speak('file "' + filename + '" is remove')
				self.reading_file_number += 1
				# the program have read all the links : next reading_file_number
				speak('Next reading file : ' + str(self.reading_file_number))
			return url

	def save_inverted_index(self, inverted_index):
		"""Save inverted-index in local

		Call after a connxion error.

		:param inverted_index: inverted-index
		:type inverted_index: dict

		"""
		speak('Save inverted-indexs in save file')
		with open(FILE_INDEX, 'w') as myfile:
			json.dump(inverted_index, myfile, ensure_ascii=False)

	def get_inverted_index(self):
		"""Get inverted-index from local

		Work only after a connxion error.

		:return: inverted-index

		"""
		speak('Get inverted-indexs in save file')
		with open(FILE_INDEX, 'r') as myfile:
			inverted_index = json.load(myfile)
		return inverted_index

	def read_inverted_index(self):
		"""Read inverted-indexs in local after safe quit

		:return: inverted-index

		"""
		speak('Get inverted-indexs in local')
		inverted_index = dict()
		for language in listdir(DIR_INDEX):
			inverted_index[language] = dict()
			for first_letter in listdir(DIR_INDEX + language):
				inverted_index[language][first_letter] = dict()
				for filename in listdir(DIR_INDEX + language + '/' + first_letter):
					with open(DIR_INDEX + language + '/' + first_letter + '/' + filename, 'r', encoding='utf-8') as myfile:
						inverted_index[language][first_letter][filename[:2]] = json.load(myfile)
		return inverted_index

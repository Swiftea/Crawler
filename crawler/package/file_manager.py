#!/usr/bin/python3

"""Crawler use lot a files. For example to manage configurations, stuck links...
Here is a class who manager files of crawler."""

__author__ = "Seva Nathan"

from os import remove, path, rename # remove, rename and know size of files
from configparser import ConfigParser


from package.data import MAX_LINKS, FILE_CONFIG, DIR_LINKS
from package.module import speak, stats_links

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

	def save_links(self, new_links):
		"""Save links

		Save link in a file without doublons and check if the file if full

		:param new_links: links to save
		:type new_links: list

		"""
		stats_links(str(len(new_links)))
		filename = DIR_LINKS + str(self.writing_file_number)
		if not path.exists(filename):
			links_to_add = new_links
			with open(filename, 'w', errors='replace',
				encoding='utf8') as myfile:
				myfile.write('\n'.join(links_to_add))
		else:
			with open(filename, 'r+', errors='replace',
				encoding='utf8') as myfile:
				old_links = myfile.read().split('\n')
				myfile.seek(0)
				links = old_links + new_links
				links_to_add = list()
				for link in links:
					if link not in links_to_add:
						links_to_add.append(link)
				myfile.write('\n'.join(links_to_add))

			if len(links_to_add) > self.max_links: # check the size
				self.writing_file_number += 1
				# more than {max_links} link : {writing_file_number}
				speak(
					'More {0} links : {1} : writing file {2}.'.format(
					str(self.max_links), str(len(links_to_add)),
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

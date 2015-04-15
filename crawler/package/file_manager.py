#!/usr/bin/python3

"""Unit for file management for crawler"""

__author__ = "Seva Nathan"

from os import remove, path, rename # remove, rename and know size of files
from configparser import ConfigParser


from package.data import * # to have required data
from package.module import speak, stats_links

class FileManager:
	"""A file managment for the crawler.

	methods :
	check_stop_crawling : check if the user want to stop
	get_max_links : get back the maxiaml number of links in a file
	save_meters : save meters in the config file
	check_size_files : del file if it size is over than MAX_SIZE
	save_links : save the list of links in the writing file
	check_size_writing : function who test the size of the writing file
	get_url : get the url of the next web site

	"""
	def __init__(self):
		"""build the file management"""
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
		"""Check if the user want to stop program."""
		self.config.read_file(open(FILE_CONFIG))
		self.run = self.config['DEFAULT']['run']

	def get_max_links(self):
		"""Get back the maximal number of links in a file."""
		self.config.read_file(open(FILE_CONFIG))
		self.max_links = int(self.config['DEFAULT']['max_links'])

	def save_config(self):
		"""Save config."""
		self.config['DEFAULT'] = {
			'run': self.run,
			'reading_file_number': str(self.reading_file_number),
			'writing_file_number': str(self.writing_file_number),
			'reading_line_number': str(self.reading_line_number),
			'max_links': str(self.max_links)
		}
		with open(FILE_CONFIG, 'w') as configfile:
			self.config.write(configfile)

	def check_size_files(self): # not use : don't work
		try: size = path.getsize(FILE_NEWS) # get the size
		except FileNotFoundError:
			speak('Log file is not found in check_size', 1)
		else:
			if size > MAX_SIZE:
				with  ZipFile(FILE_ARCHIVE_NEWS, 'r') as myzip:
					if len(myzip.namelist()) == 0:
						nbr_file_news = 0
					else:
						nbr_file_news = int(myzip.namelist()[len(
							myzip.namelist())-1])+1
				rename(FILE_NEWS, str(nbr_file_news))
				with ZipFile(FILE_ARCHIVE_NEWS, 'w') as myzip:
					myzip.write(str(nbr_file_news))
				remove(str(nbr_file_news))

		try: size = path.getsize(FILE_ERROR) # get the size
		except FileNotFoundError:
			# no news file
			speak('Errors file is not found in check_zize', 2)
		else:
			if size > MAX_SIZE:
				with  ZipFile(FILE_ARCHIVE_ERRORS, 'r') as myzip:
					if len(myzip.namelist()) == 0:
						nbr_file_news = 0
					else:
						nbr_file_news = int(myzip.namelist()[len(
							myzip.namelist())-1])+1
				rename(FILE_ERROR, str(nbr_file_news))
				with ZipFile(FILE_ARCHIVE_ERRORS, 'w') as myzip:
					myzip.write(str(nbr_file_news))
				remove(str(nbr_file_news))

	# other :

	def save_links(self, new_links):
		"""Save the links

		Save the link in a file without doublons,
		and check if the file if full.

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
		"""Get the url of the next page."""
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

	def get_inverted_index(self, to_read):
		print(to_read)
		inverted_index = dict()
		with open(DIR_INDEX + '_', 'r') as myfile:
			inverted_index['_'] = myfile.read()
		for letter_index in to_read:
			with open(DIR_INDEX + letter_index, 'r') as myfile:
				inverted_index[letter_index] = myfile.read()
		return inverted_index
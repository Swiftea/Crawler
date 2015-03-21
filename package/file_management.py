#!/usr/bin/python3

"""Unit for file management for crawler"""

__author__ = "Seva Nathan"

from os import remove, path, rename # remove file and know it size
import json # to save documents not sending
from configparser import ConfigParser
from zipfile import ZipFile


from package.data import * # to have required datas
from package.module import speak, stats_links

class FileManagement:
	"""A file managment for the crawler.

	methodes : 
	often and sometimes are methodes that group other methodes.
	sometimes : get_nbr_max, save_meters, check_size_files
	get_meters : get back meters : writing file, reading file, link lines in reading file
	line of links, maximal nuimber of links in a file
	get_stop : check if the user want to stop
	get_nbr_max : get back the maxiaml number of links in a file
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
		self.links_number = LINKS_NUMBER # number of maximum links in a file
		self.run = True # run program bool
		self.config = ConfigParser()

		if not path.exists(FILE_CONFIG):
			self.config['DEFAULT'] = {
				'run': True,
				'reading_file_number': '0',
				'writing_file_number': '1',
				'reading_line_number': '0',
				'links_number': LINKS_NUMBER
			}
	
			with open(FILE_CONFIG, 'w') as configfile:
				self.config.write(configfile)
		else:
			self.config.read_file(open(FILE_CONFIG))
			self.run = bool(self.config['DEFAULT']['run'])
			self.reading_file_number = int(self.config['DEFAULT']['reading_file_number'])
			self.writing_file_number = int(self.config['DEFAULT']['writing_file_number'])
			self.reading_line_number = int(self.config['DEFAULT']['reading_line_number'])
			self.links_number = int(self.config['DEFAULT']['links_number'])


		# un peu dégeulasse : (?)
		with ZipFile(FILE_ARCHIVE_NEWS, 'w') as myzip:
			pass # create zip file
		with ZipFile(FILE_ARCHIVE_ERRORS, 'w') as myzip:
			pass # create zip file

		self.get_stop()
		self.get_nbr_max()

	def sometimes(self):
		"""When a links file is fulled."""
		self.get_stop()
		self.get_nbr_max()
		self.save_meters()
		#self.check_size_files() # don't work well ! (?)

	# sometimes : 

	def get_stop(self):
		"""Check if the user want to stop program."""
		self.config.read_file(open(FILE_CONFIG))
		self.run = bool(self.config['DEFAULT']['run'])

	def get_nbr_max(self):
		"""Get back the maximal number of links in a file."""
		self.config.read_file(open(FILE_CONFIG))
		self.links_number = int(self.config['DEFAULT']['links_number'])
	
	def save_meters(self):
		"""Save meters in the config file."""
		self.config['DEFAULT'] = {
			'run': str(self.run),
			'reading_file_number': str(self.reading_file_number),
			'writing_file_number': str(self.writing_file_number),
			'reading_line_number': str(self.reading_line_number),
			'links_number': str(self.links_number)
		}
		with open(FILE_CONFIG, 'w') as configfile:
			self.config.write(configfile)
	
	def check_size_files(self):
		"""Alerte if size of files is over than MAX_SIZE."""
		try: size = path.getsize(FILE_NEWS) # get the size
		except FileNotFoundError:
			speak('fichier journal introuvable dans check_size', 1)
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
			speak('fichier erreurs introuvable dans check_size', 2)
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
		"""Save the link in a file without doublons,
		and check if the file if full."""
		stats_links(str(len(new_links)))
		file_name = DIR_LINKS + str(self.writing_file_number)
		if not path.exists(file_name):
			links_to_add = new_links
			with open(file_name, 'w', errors='replace',
				encoding='utf8') as myfile:
				myfile.write('\n'.join(links_to_add))
		else:
			with open(file_name, 'r+', errors='replace',
				encoding='utf8') as myfile:
				old_links = myfile.read().split()
				myfile.seek(0)
				links_to_add = list(set(old_links + new_links))
				myfile.write('\n'.join(links_to_add))
			if len(links_to_add) > self.links_number: # check the size
				self.writing_file_number += 1
				speak(
					'plus de {0} liens : {1} : fichier écriture {2}.'.format(
					str(self.links_number), str(len(links_to_add)),
					str(self.writing_file_number))
				)

	def get_url(self):
		"""Get the url of the next page."""
		# joining : /liens/(reading meter) : 
		file_name = DIR_LINKS + str(self.reading_file_number)
		try:
			with open(file_name, 'r', errors='replace',
				encoding='utf8') as myfile:
				list_links = myfile.read().split() # list of urls
		except FileNotFoundError:
			speak('fichier lecture introuvable dans get_url : ' + file_name, 4)
			return 'stop'
		else:
			url = list_links[self.reading_line_number]
			self.reading_line_number += 1
			if len(list_links) == (self.reading_line_number): # if is the last links of the file
				self.reading_line_number = 0
				if self.reading_file_number != 0: # or > 0 ? lequel est le plus rapide
					remove(file_name)
					speak('fichier ' + file_name + ' supprimé')
				self.reading_file_number += 1
				speak('fichier lecture suivant : ' + str(self.reading_file_number))
			return url

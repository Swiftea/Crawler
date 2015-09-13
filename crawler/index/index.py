#!/usr/bin/python3

"""Define several functions for inverted-index."""

from swiftea_bot.data import DIR_DATA

def count_files(index):
	"""Return number of file to download are uplaod

	:return: int

	"""
	nb_files = int()
	for language in index:
		for first_letter in index[language]:
			for two_letters in index[language][first_letter]:
				nb_files += 1
	return nb_files

def stats_dl_index(begining, end):
	"""Write the time to download inverted-index.

	:param begining: time download inverted-index
	:type begining: int
	:param end: time after download inverted-index
	:type end: int

	"""
	with open(DIR_DATA + 'stat_dl_index', 'a') as myfile:
		myfile.write(str(end - begining) + '\n')

def stats_ul_index(begining, end):
	"""Write the time to upload inverted-index.

	:param begining: time before send inverted-index
	:type begining: int
	:param end: time after send inverted-index
	:type end: int

	"""
	with open(DIR_DATA + 'stat_up_index', 'a') as myfile:
		myfile.write(str(end - begining) + '\n')

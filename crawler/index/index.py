#!/usr/bin/env python3

"""Define several functions for inverted-index."""

from crawler.swiftea_bot.data import DIR_STATS


def count_files_index(index):
	"""Return number of file to download are upload.

	Parse languages and letters from the given index.

	:return: int

	"""
	nb_files = int()
	for language in index:
		for first_letter in index[language]:
			nb_files += len(index[language][first_letter])
	return nb_files


def stats_dl_index(begining, end):
	"""Write the time to download inverted-index.

	:param begining: time download inverted-index
	:type begining: int
	:param end: time after download inverted-index
	:type end: int

	"""
	with open(DIR_STATS + 'stat_dl_index', 'a') as myfile:
		myfile.write(str(end - begining) + '\n')


def stats_ul_index(begining, end):
	"""Write the time to upload inverted-index.

	:param begining: time before send inverted-index
	:type begining: int
	:param end: time after send inverted-index
	:type end: int

	"""
	with open(DIR_STATS + 'stat_up_index', 'a') as myfile:
		myfile.write(str(end - begining) + '\n')

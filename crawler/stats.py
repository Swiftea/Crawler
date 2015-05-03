#!/usr/bin/python3

"""Display stats."""

import package.data as data
from package.module import average

def stats():
	try:
		with open(data.DIR_DATA + 'stat_stopwords', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:  # noqa
		stat_stopwords = 'File ' + data.DIR_DATA + 'stat_stopwords' + ' not found.'
	else:
		stat_stopwords = 'Average percentage of removed words: ' + str(average(content))
		if len(content) > 10000:
			compress_stats(data.DIR_DATA + 'stat_stopwords')
	result = stat_stopwords + '\n'
	try:
		with open(data.DIR_DATA + 'stat_links', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:  # noqa
		stat_links = ('File ' +  data.DIR_DATA + 'stat_links' + ' not found.')
	else:
		stat_links = ('Average links in webpage: ' + str(average(content)))
		if len(content) > 10000:
			compress_stats(data.DIR_DATA + 'stat_links')
	result += stat_links + '\n'
	try:
		with open(data.DIR_DATA + 'stat_webpages', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:  # noqa
		stat_webpages = 'File ' +  data.DIR_DATA + 'stat_webpages' + ' not found.'
	else:
		stat_webpages = 'Time to crawl ten webpages: ' + str(average(content))
	result += stat_webpages + '\n'
	try:
		with open(data.DIR_DATA + 'stat_dl_index', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:  # noqa
		stat_dl_index = 'File ' +  data.DIR_DATA + 'stat_dl_index' + ' not found.'
	else:
		stat_dl_index = 'Time upload inverted-index: ' + str(average(content))
	result += stat_dl_index + '\n'
	try:
		with open(data.DIR_DATA + 'stat_up_index', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:  # noqa
		stat_up_index = 'File ' +  data.DIR_DATA + 'stat_up_index' + ' not found.'
	else:
		stat_up_index = 'Time download inverted-index: ' + str(average(content))
	result += stat_up_index + '\n'
	return result

def compress_stats(filename):
	with open(filename, 'r+') as myfile:
		content = average(myfile.read().split())
		myfile.seek(0)
		myfile.write(str(content))

if __name__ == '__main__':
	print(stats())

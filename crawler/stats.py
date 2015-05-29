#!/usr/bin/python3

"""Display stats."""

from swiftea_bot.data import DIR_DATA

def stats():
	try:
		with open(DIR_DATA + 'stat_stopwords', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:  # pylint:disable=undefined-variable
		stat_stopwords = 'File ' + DIR_DATA + 'stat_stopwords' + ' not found.'
	else:
		stat_stopwords = 'Average percentage of removed words: ' + str(average(content))
		if len(content) > 10000:
			compress_stats(DIR_DATA + 'stat_stopwords')
	result = stat_stopwords + '\n'
	try:
		with open(DIR_DATA + 'stat_links', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:  # pylint:disable=undefined-variable
		stat_links = ('File ' +  DIR_DATA + 'stat_links' + ' not found.')
	else:
		stat_links = ('Average links in webpage: ' + str(average(content)))
		if len(content) > 10000:
			compress_stats(DIR_DATA + 'stat_links')
	result += stat_links + '\n'
	try:
		with open(DIR_DATA + 'stat_webpages', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:  # pylint:disable=Undefined-variable
		stat_webpages = 'File ' +  DIR_DATA + 'stat_webpages' + ' not found.'
	else:
		stat_webpages = 'Time to crawl ten webpages: ' + str(average(content))
	result += stat_webpages + '\n'
	try:
		with open(DIR_DATA + 'stat_dl_index', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:  # pylint:disable=Undefined-variable
		stat_dl_index = 'File ' +  DIR_DATA + 'stat_dl_index' + ' not found.'
	else:
		stat_dl_index = 'Time upload inverted-index: ' + str(average(content))
	result += stat_dl_index + '\n'
	try:
		with open(DIR_DATA + 'stat_up_index', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:  # pylint:disable=Undefined-variable
		stat_up_index = 'File ' +  DIR_DATA + 'stat_up_index' + ' not found.'
	else:
		stat_up_index = 'Time download inverted-index: ' + str(average(content))
	result += stat_up_index + '\n'
	return result

def compress_stats(filename):
	with open(filename, 'r+') as myfile:
		content = average(myfile.read().split())
		myfile.seek(0)
		myfile.write(str(content))

def average(content):
	"""Calculate average.

	:param content: values
	:type content: list
	:return: average

	"""
	total = 0
	for value in content:
		total += float(value)
	moy = total / len(content)
	return moy

if __name__ == '__main__':
	print(stats())

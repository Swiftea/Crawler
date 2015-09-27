#!/usr/bin/python3

"""Display stats."""

from swiftea_bot.data import DIR_DATA

def stats(dir_data=DIR_DATA):
	try:
		with open(dir_data + 'stat_stopwords', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:
		stat_stopwords = 'File ' + dir_data + 'stat_stopwords' + ' not found.'
	else:
		stat_stopwords = 'Average percentage of removed words: ' + str(average(content))
		if len(content) > 10000:
			compress_stats(dir_data + 'stat_stopwords')
	result = stat_stopwords + '\n'
	try:
		with open(dir_data + 'stat_links', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:
		stat_links = ('File ' +  dir_data + 'stat_links' + ' not found.')
	else:
		stat_links = ('Average links in webpage: ' + str(average(content)))
		if len(content) > 10000:
			compress_stats(dir_data + 'stat_links')
	result += stat_links + '\n'
	try:
		with open(dir_data + 'stat_webpages', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:
		stat_webpages = 'File ' +  dir_data + 'stat_webpages' + ' not found.'
	else:
		stat_webpages = 'Time to crawl ten webpages: ' + str(average(content))
	result += stat_webpages + '\n'
	try:
		with open(dir_data + 'stat_dl_index', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:
		stat_dl_index = 'File ' +  dir_data + 'stat_dl_index' + ' not found.'
	else:
		stat_dl_index = 'Time download inverted-index: ' + str(average(content))
	result += stat_dl_index + '\n'
	try:
		with open(dir_data + 'stat_up_index', 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:
		stat_up_index = 'File ' +  dir_data + 'stat_up_index' + ' not found.'
	else:
		stat_up_index = 'Time upload inverted-index: ' + str(average(content))
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
	return round(moy, 2)

if __name__ == '__main__':
	print(stats())

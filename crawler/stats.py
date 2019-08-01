#!/usr/bin/env python3

"""Display stats."""

from os.path import exists


from crawler.swiftea_bot.data import DIR_STATS


def stats(dir_stats=DIR_STATS):
	"""Return a report of average statistics stored in data/stats."""
	if exists(dir_stats + 'stat_links'):
		with open(dir_stats + 'stat_links', 'r') as myfile:
			content = myfile.read().split()
		stat_links = ('Average links in webpage: ' + str(average(content)))
		if len(content) > 10000:
			compress_stats(dir_stats + 'stat_links')
	else:
		stat_links = ('File ' + dir_stats + 'stat_links' + ' not found.')
	result = stat_links + '\n'

	if exists(dir_stats + 'stat_webpages'):
		with open(dir_stats + 'stat_webpages', 'r') as myfile:
			content = myfile.read().split()
		stat_webpages = 'Time to crawl n webpages: ' + str(average(content))
	else:
		stat_webpages = 'File ' + dir_stats + 'stat_webpages' + ' not found.'
	result += stat_webpages + '\n'

	if exists(dir_stats + 'stat_crawl_one_webpage'):
		with open(dir_stats + 'stat_crawl_one_webpage', 'r') as myfile:
			content = myfile.read().split()
		stat_crawl_one_webpage = 'Time to crawl n stat_crawl_one_webpage: ' + str(average(content))
	else:
		stat_crawl_one_webpage = 'File ' + dir_stats + 'stat_crawl_one_webpage' + ' not found.'
	result += stat_crawl_one_webpage + '\n'

	if exists(dir_stats + 'stat_dl_index'):
		with open(dir_stats + 'stat_dl_index', 'r') as myfile:
			content = myfile.read().split()
		stat_dl_index = 'Time download inverted-index: ' + str(average(content))
	else:
		stat_dl_index = 'File ' + dir_stats + 'stat_dl_index' + ' not found.'
	result += stat_dl_index + '\n'

	if exists(dir_stats + 'stat_up_index'):
		with open(dir_stats + 'stat_up_index', 'r') as myfile:
			content = myfile.read().split()
		stat_up_index = 'Time upload inverted-index: ' + str(average(content))
	else:
		stat_up_index = 'File ' + dir_stats + 'stat_up_index' + ' not found.'
	result += stat_up_index + '\n'

	return result


def compress_stats(filename):
	"""Erase the `filename` and write the average value."""
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

#!/usr/bin/env python3

"""Define several functions for WebConnection."""

import requests


from crawler.swiftea_bot.module import remove_duplicates, tell
from crawler.crawling.searches import clean_link


def check_connection(url='https://github.com'):
	"""Test internet connection.

	Try to connect to a website.

	:param url: url used to test the connection
	:return: True if connected to internet

	"""
	try:
		requests.get(url)
	except requests.exceptions.RequestException:
		tell('No connection')
		return False
	else:
		return True


def is_nofollow(url):
	"""Check if take links.

	Search !nofollow! at the end of url, remove it if found.

	:param url: webpage url
	:type url: str
	:return: True if nofollow and url

	"""
	if url.endswith('!nofollow!'):
		return True, url[:-10]

	return False, url


def duplicate_content(code1, code2):
	"""Compare code1 and code2.

	:param code1: first code to compare
	:type code1: str
	:param code2: second code to compare
	:type code2: str

	"""
	if code1 != code2:
		size_code1, size_code2 = len(code1), len(code2)
		# Percent of similar words
		similar_words = 0
		if size_code1 < size_code2:
			keywords_code2 = code2.split()
			for keyword in code1.split():
				if keyword in keywords_code2:
					similar_words += 1
			percent = similar_words * 100 / len(keywords_code2)
		else:
			keywords_code1 = code1.split()
			for keyword in code2.split():
				if keyword in keywords_code1:
					similar_words += 1
			percent = similar_words * 100 / len(keywords_code1)

		if percent >= 95:
			is_duplicate = True
		elif 65 < percent < 95:
			# Advanced verification to confirm or not
			# Difference percent of size.
			difference = 15
			if size_code1 > size_code2:
				size_code2, size_code1 = size_code1, size_code2
			percent_difference = (size_code2 - size_code1) * 100 / size_code2

			is_duplicate = percent_difference <= difference
		else:
			is_duplicate = False
	else:
		is_duplicate = True

	return is_duplicate


def all_urls(request):
	"""Return all urls from request.history.

	:param request: request
	:type request: requests.models.Response
	:param first: list start with the url if given
	:type first: str
	:return: list of redirected urls, first is the last one

	"""
	list_urls = [clean_link(request.url)]
	for req in request.history:
		list_urls.append(clean_link(req.url))
	urls = list()
	for url in list_urls:
		if url:
			urls.append(url)
	return remove_duplicates(urls)


def clean_links(links, base_url=None):
	"""Clean webpage's links: rebuild urls with base url and
	remove anchors, mailto, javascript, .index.

	:param links: links to clean
	:type links: list
	:return: cleanen links without duplicate

	"""
	links = remove_duplicates(links)
	new_links = list()

	for url in links:
		new_url = clean_link(url, base_url)
		if new_url:
			new_links.append(new_url)

	return remove_duplicates(new_links)


def clean_favicon(favicon, base_url):
	"""Clean favicon.

	:param favicon: favicon url to clean
	:type favicon: str
	:return: cleaned favicon

	"""
	if not favicon.startswith('http') and not favicon.startswith('www'):
		if favicon.startswith('//'):
			favicon = 'http:' + favicon
		elif favicon.startswith('/'):
			favicon = base_url + favicon
		else:
			favicon = base_url + '/' + favicon

	return favicon

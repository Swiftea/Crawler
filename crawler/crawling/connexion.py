#!/usr/bin/python3

"""Define several functions WebConnexion."""

import requests

from swiftea_bot.module import remove_duplicates
from crawling.searches import clean_link
from swiftea_bot.module import tell
from swiftea_bot.data import LANGUAGES, HOST

def no_connexion(url='https://github.com'):
	"""Check connexion.

	Try to connect to swiftea website.

	:param url: url use by test
	:return: True if no connexion

	"""
	try:
		requests.get(url)
	except requests.exceptions.RequestException:
		tell('No connexion')
		return True
	else:
		return False

def is_nofollow(url):
	"""Check if take links.

	Search !nofollow! at the end of url, remove it if found.

	:param url: webpage url
	:type url: str
	:return: True if nofollow and url

	"""
	if url.endswith('!nofollow!'):
		return True, url[:-10]
	else:
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
		elif percent >= 65 and percent < 95:
			# Advanced verification to confirm or not
			# Difference percent of size.
			difference = 15
			if size_code1 > size_code2:
				percent_difference = (size_code1 - size_code2) * 100 / size_code1
				if percent_difference <= difference:
					is_duplicate = True
				else:
					is_duplicate = False
			else:
				percent_difference = (size_code2 - size_code1) * 100 / size_code2
				if percent_difference <= difference:
					is_duplicate = True
				else:
					is_duplicate = False
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

#!/usr/bin/env python3

"""After parsing source code, extracted data must be classified and cleaned.
Here is a class that use the html parser and manage all results."""

from urllib.parse import urlparse

from crawler.swiftea_bot.module import tell, remove_duplicates
from crawler.crawling import parsers, searches, data_processing


class SiteInformations:
	"""Class to manage searches in source code."""
	def __init__(self):
		"""Build searches manager."""
		self.parser = parsers.ExtractData()
		self.STOPWORDS = None
		self.BADWORDS = None

	def set_listswords(self, stopwords, badwords):
		self.STOPWORDS = stopwords
		self.BADWORDS = badwords

	def get_infos(self, url, code, nofollow, score):
		"""Manage all searches of webpage's informations.

		:param url: url of webpage
		:type url: str
		:param score: score of webpage
		:type score: int
		:param code: source code of webpage
		:type code: str
		:param nofollow: if we take links of webpage
		:type nofollow: bool
		:return: links, title, description, key words, language,
			score, number of words

		"""
		results = dict()
		results['homepage'] = 1 if searches.is_homepage(url) else 0

		self.parser.feed(code)

		results['title'] = searches.clean_text(searches.capitalize(self.parser.title))  # Find title and clean it

		keywords = searches.clean_text(self.parser.keywords.lower()).split()

		# Language:
		if self.parser.language != '':
			language = self.parser.language
			score += 1
		else:
			language = self.detect_language(keywords)

		if language in self.STOPWORDS and self.parser.title != '':
			keywords = self.clean_keywords(keywords, language)
			keywords.extend(self.clean_keywords(results['title'].lower().split(), language))
			infos_url = urlparse(url)
			path_position = infos_url.path.rfind('.')
			path = infos_url.path[:path_position]
			keywords.extend(self.clean_keywords(path, language))

			results['sanesearch'] = self.sane_search(keywords, language)
			results['language'] = language
			results['keywords'] = keywords

			# Description:
			if self.parser.description == '':
				results['description'] = searches.clean_text(searches.capitalize(self.parser.first_title))
			else:
				results['description'] = searches.clean_text(searches.capitalize(self.parser.description))

			# Css:
			if self.parser.css:
				score += 1

			base_url = searches.get_base_url(url)

			# Links:
			if nofollow:
				links = list()
			else:
				links = data_processing.clean_links(self.parser.links, base_url)
				searches.stats_links(len(links))
			if self.parser.favicon != '':
				results['favicon'] = self.clean_favicon(self.parser.favicon, base_url)
			else:
				results['favicon'] = ''
		else:
			tell('No language or title', severity=-1)
			results = {'title': ''}
			links = list()
			results['language'] = '*'

		results['score'] = score
		return results, links

	def detect_language(self, keywords):
		"""Detect language of webpage if not given.

		:param keywords: keywords of webpage used for detecting
		:type keywords: list
		:return: language found

		"""
		total_stopwords = 0

		# Number stopwords
		nb_stopwords = dict()
		for lang in self.STOPWORDS:
			nb_stopwords[lang] = 0

			for keyword in keywords:
				if keyword in self.STOPWORDS[lang]:
					total_stopwords += 1
					nb_stopwords[lang] += 1

		if total_stopwords != 0:
			language = max(nb_stopwords, key=nb_stopwords.get)
		else:
			language = ''

		return language

	def clean_favicon(self, favicon, base_url):
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

	def clean_keywords(self, dirty_keywords, language):
		"""Clean found keywords.

		Delete stopwords, bad chars, two letter less word and split word1-word2

		:param keywords: keywords to clean
		:type keywords: list
		:return: list of cleaned keywords

		"""
		stopwords = self.STOPWORDS[language]
		cleaned_keywords = list()
		half_cleaned_keywords = list()  # cleaning with regex (with '_')
		for keyword in dirty_keywords:
			half_cleaned_keywords.extend(searches.regex.findall(keyword))
		new_keywords = list()  # Without '_'
		for keyword in half_cleaned_keywords:
			new_keywords.extend(keyword.split('_'))
		for keyword in new_keywords:
			if keyword not in stopwords and len(keyword) > 1:
				cleaned_keywords.append(keyword)
		# calculate occurrence
		keywords_done = list()
		keywords = list()
		for keyword in cleaned_keywords:
			if keyword not in keywords_done:
				keywords.append((keyword, cleaned_keywords.count(keyword)))
				keywords_done.append(keyword)
		return keywords

	def sane_search(self, keywords, language, max_ratio=.2):
		"""Filter pages not suitable for a young audience.

		:param: keywords: webpage's keywords
		:type keywords: list
		:pram language: found website language
		:type language: str
		:return: True or False

		"""
		badwords = self.BADWORDS[language]
		nb_badwords = 0
		nb_words = len(keywords)
		if nb_words == 0:
			return False
		for keyword in keywords:
			if keyword in badwords:
				nb_badwords += 1
		ratio = nb_badwords / nb_words
		if ratio >= max_ratio:
			tell('bad site detected')
			return True
		return False

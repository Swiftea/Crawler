#!/usr/bin/python3

"""After parse source code, data extracted must be classify and clean.
Here is a class who use the html parser and manage all results."""

import package.module as module
from package.parsers import MyParser

class SiteInformations(object):
	"""Class to manage searches in source codes."""
	def __init__(self):
		"""Build searches manager"""
		self.parser = MyParser()
		self.STOPWORDS = module.get_stopwords()


	def get_infos(self, url, code, nofollow, score):
		"""Manager all searches of webpage's informations.

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
		homepage = 1 if module.is_homepage(url) else 0

		self.parser.feed(code)

		title = module.clean_text(self.parser.title.capitalize())  # Find title and clean it

		keywords = module.clean_text(self.parser.keywords.lower()).split()
		begining_size = len(keywords)  # Stats

		# Language:
		if self.parser.language != '':
			language = self.parser.language
			score += 1
		else:
			language = self.detect_language(keywords, url)

		if language in self.STOPWORDS and self.parser.title != '':
			keywords = self.clean_keywords(keywords, language)
			keywords.extend(self.clean_keywords(title.lower().split(), language))

			# Description:
			if self.parser.description == '':
				description = module.clean_text(self.parser.first_title.capitalize())
			else:
				description = module.clean_text(self.parser.description.capitalize())

			# Css:
			if self.parser.css:
				score += 1

			module.stats_stop_words(begining_size, len(keywords))  # stats

			base_url = module.get_base_url(url)

			# Links:
			if nofollow:
				links = list()
			else:
				links = self.clean_links(self.parser.links, base_url)

			# Favicon:
			if self.parser.favicon != '':
				favicon = self.clean_favicon(self.parser.favicon, base_url)
			else:
				favicon = ''
		else:
			module.tell('No language or title', severity=-1)
			title = links = description = score = favicon = ''

		return links, title, description, keywords, language, score, favicon, homepage


	def detect_language(self, keywords, url):
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

		with open('output/detect_language', 'a') as myfile:
			myfile.write(language + ': ' + url + '\n')
		return language


	def clean_links(self, links, base_url=None):
		"""Clean webpage's links: rebuild urls with base url and
		remove anchors, mailto, javascript, .index.

		:param links: links to clean
		:type links: list
		:return: cleanen links without duplicate

		"""
		links = module.remove_duplicates(links)
		new_links = list()

		for url in links:
			new_url = module.clean_link(url, base_url)
			if new_url:
				new_links.append(new_url)

		return module.remove_duplicates(new_links)


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


	def clean_keywords(self, keywords, language):
		"""Clean found keywords.

		Delete stopwords, bad chars, two letter less word and split word1-word2

		:param keywords: keywords to clean
		:type keywords: list
		:return: list of cleaned keywords

		"""
		stopwords = self.STOPWORDS[language]
		new_keywords = []
		for keyword in keywords:
			if module.check_size_keyword(keyword):
				if module.letter_repeat(keyword):
					continue
				keyword = module.remove_useless_chars(keyword)
				if keyword is None:
					continue
				if module.is_letters(keyword):
					continue

				is_list, keywords = module.split_keywords(keyword)
				if is_list:
					keywords = self.clean_keywords(keywords, language)

				if keyword not in stopwords:
					new_keywords.append(keyword)
		return new_keywords

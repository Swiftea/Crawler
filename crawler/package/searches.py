#!/usr/bin/python3

"""After parse source code, data extracted must be classify and clean.
Here is a class who use the html parser and manage all results."""

from urllib.parse import urlparse

import package.data as data
import package.module as module
from package.parsers import MyParser

class SiteInformations(object):
	"""Class to manage searches in source codes."""
	def __init__(self):
		"""Build searches manager"""
		self.parser = MyParser()
		self.url = str()
		self.score = float()
		self.title = str()
		self.description = str()
		self.language = str()
		self.links = list()
		self.keywords = list()
		self.code = str()
		self.new = str()
		self.slash = int()
		self.favicon = str()
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
		self.url = url
		self.score = score

		self.parser.feed(code)

		self.title = module.clean_text(self.parser.title)  # Find title and clean it

		keywords = module.clean_text(self.parser.keywords.lower()).split()
		begining_size = len(keywords)  # Stats

		# Language:
		if self.parser.language != '':
			self.language = self.parser.language
			self.score += 0.5
		else:
			self.language = self.detect_language(keywords)

		if self.language in self.STOPWORDS and self.parser.title != '':
			self.keywords = self.clean_keywords(keywords)
			self.keywords.extend(self.clean_keywords(self.title.lower().split()))

			# Description:
			if self.parser.description == '':
				self.description = module.clean_text(self.parser.first_title)
			else:
				self.description = module.clean_text(self.parser.description)

			# Css:
			if self.parser.css:
				self.score += 0.5

			module.stats_stop_words(begining_size, len(self.keywords))  # stats

			# Links:
			if nofollow:
				self.links = list()
				module.speak('No take links')  # why ?
			else:
				self.links = self.clean_links(self.parser.links)

			# Favicon:
			if self.parser.favicon != '':
				self.favicon = self.clean_favicon(self.parser.favicon)
			else:
				self.favicon = ''
		else:
			module.speak('No language or title')
			self.title = ''
			self.links = self.description = self.keywords = self.language = self.score = self.favicon = None

		return self.links, self.title, self.description, self.keywords, self.language, self.score, self.favicon


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

		if nb_stopwords and total_stopwords != 0:
			language = max(nb_stopwords, key=nb_stopwords.get)
			percent = round(nb_stopwords[language] * 100 / total_stopwords)

			if(percent < 30):
				language = ''
		else:
			language = ''

		return language


	def clean_links(self, links):
		"""Clean webpage's links: rebuild urls with base url and
		remove anchors, mailto, javascript, .index.

		:param links: links to clean
		:type links: list
		:return: cleanen links without duplicate

		"""
		links = module.remove_duplicates(links)
		new_links = list()

		for url in links:
			new = url.strip()  # Link to add in new list of links
			if (not new.endswith(data.BAD_EXTENTIONS) and
				new != '/' and
				new != '#' and
				not new.startswith('mailto:') and
				'javascript:' not in new and
				new != ''):
				if not new.startswith('http') and not new.startswith('www'):
					base_url = module.get_base_url(self.url)
					if new.startswith('//'):
						new = 'http:' + new
					elif new.startswith('/'):
						new = base_url + new
					else:
						new = base_url + '/' + new
				# Delete anchors:
				infos_url = urlparse(new)
				new = infos_url.scheme + '://' + infos_url.netloc + infos_url.path
				if new.endswith('/'):
					new = new[:-1]
				nb_index = new.find('index.')
				if nb_index != -1:
					new = new[:nb_index]
				if infos_url.query != '':
					new += '?' + infos_url.query
				new_links.append(new)

		return module.remove_duplicates(new_links)


	def clean_favicon(self, favicon):
		"""Clean favicon.

		:param favicon: favicon url to clean
		:type favicon: str
		:return: cleaned favicon

		"""
		base_url = module.get_base_url(self.url)
		if not favicon.startswith('http') and not favicon.startswith('www'):
			if favicon.startswith('//'):
				favicon = 'http:' + favicon
			elif favicon.startswith('/'):
				favicon = base_url + favicon
			else:
				favicon = base_url + '/' + favicon

		return favicon


	def clean_keywords(self, keywords):
		"""Clean found keywords.

		Delete stopwords, bad chars, two letter less word and split word1-word2

		:param keywords: keywords to clean
		:type keywords: list
		:return: list of cleaned keywords

		"""
		stopwords = self.STOPWORDS[self.language]
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
					keywords = self.clean_keywords(keywords)

				if keyword not in stopwords:
					new_keywords.append(keyword)
		return new_keywords

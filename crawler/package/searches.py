#!/usr/bin/python3

"""Searches class :

MyParser is the html parser,
SiteInformations groups methodes for informations of the page.

"""

__author__ = "Seva Nathan"

from urllib.parse import urlparse


from package.data import * # to have required data
from package.module import speak, stats_stop_words, get_stopwords, clean_text, remove_duplicates, get_base_url
from package.parsers import MyParser
class SiteInformations:
	def __init__(self):
		"""Build the class : define variables."""
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
		self.nb_words = int()
		self.favicon = str()

	def get_stopwords(self):
		self.STOPWORDS = get_stopwords()
		if self.STOPWORDS == dict():
			# no STOPWORDS : the program will stop
			speak('STOPWORDS is null, quit program')
			return False
		else:
			return True

	def get_infos(self, url, code, nofollow, score):
		"""Get all webpage's informations.

		url : the url of the page
		score : the score of the page
		code : the source code of the page
		faviconnofollow : if we take the links of the page
		return : list of links, title, description, key words, language,
			score, number of words

		"""
		self.url = url
		self.score = score

		self.parser.feed(code)

		self.title = clean_text(self.parser.title) # find title and clean it

		keywords = clean_text(self.parser.keywords.lower()).split()
		begining_size = len(keywords) # stats

		# language :
		if self.parser.language != '':
			self.language = self.parser.language
			self.score += 0.5
		else:
			self.language = self.detect_language(keywords)

		if self.language in self.STOPWORDS and self.parser.title != '':
			self.keywords = self.clean_keywords(keywords)
			self.keywords.extend(self.clean_keywords(self.title.lower().split()))

			# description :
			if self.parser.description == '':
				self.description = clean_text(self.parser.first_title)
			else:
				self.description = clean_text(self.parser.description)

			# css :
			if self.parser.css:
				self.score += 0.5

			self.nb_words = len(self.keywords)
			stats_stop_words(begining_size, self.nb_words) # stats

			# links :
			if nofollow:
				self.links = list()
				speak('No take links') # why ?
			else:
				self.links = self.clean_links(self.parser.links)

			# favicon :
			if self.parser.favicon != '':
				self.favicon = self.clean_favicon(self.parser.favicon)
			else:
				self.favicon = ''
		else:
			speak('No language or title')
			self.title = ''
			self.links = self.description = self.keywords = self.language = self.score = self.nb_words = self.favicon = None

		return self.links, self.title, self.description, self.keywords, self.language, self.score, self.nb_words, self.favicon

	def detect_language(self, keywords):
		total_stopwords = 0

	    # Nb stopwords
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
		"""Clean the list of links.

		new : the links to add in the new list of links

		"""
		links = remove_duplicates(links)
		new_links = list()

		for i, url in enumerate(links):
			new = url.strip()
			if (not new.endswith(BAD_EXTENTIONS) and
				new != '/' and
				new != '#' and
				not new.startswith('mailto:') and
				not 'javascript:' in new and
				new != ''):
				if not new.startswith('http') and not new.startswith('www'):
					base_url = get_base_url(self.url)
					if new.startswith('//'):
						new = 'http:' + new
					elif new.startswith('/'):
						new = base_url + new
					else:
						new = base_url + '/' + new
				# delete anchors :
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

		return remove_duplicates(new_links)

	def clean_favicon(self, favicon):
		base_url = get_base_url(self.url)
		if not favicon.startswith('http') and not favicon.startswith('www'):
			if favicon.startswith('//'):
				favicon = 'http:' + favicon
			elif favicon.startswith('/'):
				favicon = base_url + favicon
			else:
				favicon = base_url + '/' + favicon
		return favicon

	def clean_keywords(self, keywords):
		"""Clean found keywords."""
		if self.language == 'fr':
			stopwords = self.STOPWORDS['fr']
		elif self.language == 'en':
			stopwords = self.STOPWORDS['en']
		elif self.language == 'es':
			stopwords = self.STOPWORDS['es']
		elif self.language == 'it':
			stopwords = self.STOPWORDS['it']
		else:
			stopwords = []
		result = []
		for keyword in keywords:
			# 2 chars at least and check if word is not only special chars
			if len(keyword) > 2 and not keyword.isnumeric():
				# remove useless chars
				if keyword.startswith(START_CHARS):
					keyword = keyword[1:]

				if keyword.endswith(END_CHARS):
					keyword = keyword[:-1]
				if keyword.endswith(END_CHARS2):
					keyword = keyword[:-3]

				if len(keyword) > 1: # l', d', s'
					if keyword[1] == '\'' or keyword[1] == '’':
						keyword = keyword[2:]
				if len(keyword) > 2:
					if keyword[-2] == '\'': # word's
						keyword = keyword[:-2]

				point = keyword.find('.')
				if point != -1:
					keyword = keyword[:point]

				if not True in [letter in keyword for letter in ALPHABET]:
					continue

				if not True in [letter != '' for letter in keyword.split(keyword[0])]:
					continue# keyword = '********'

				if keyword.endswith(END_CHARS): # repeat end chars
					keyword = keyword[:-1]

				# word/word2
				if '/' in keyword:
					keyword = keyword.split('/') # str -> list
					for word in keyword:
						if len(word) > 2  and word not in stopwords:
							result.append(word)
				else:
					if len(keyword) > 2  and keyword not in stopwords:
						result.append(keyword)
		return result
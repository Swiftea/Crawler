#!/usr/bin/python3

"""Searches class :

MyParser is the html parser,
SiteInformations groups methodes for informations of the page.

"""

__author__ = "Seva Nathan"

from urllib.parse import urlparse


from package.data import * # to have required data
from package.module import speak, stats_stop_words, get_stopwords

class SiteInformations:
	def __init__(self):
		"""Build the class : define variables."""
		self.url = str()
		self.score = float()
		self.title = str()
		self.description = str()
		self.language = str()
		self.links = list()
		self.keywords = list()
		self.parser = MyParser()
		self.code = str()
		self.new = str()
		self.slash = int()
		self.urlparse = None
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
		nofollow : if we take the links of the page
		return : list of links, title, description, key words, language,
			score, number of words

		"""
		self.url = url
		self.score = score

		self.parser.feed(code)

		if self.parser.title != '':
			self.title = self.clean_text(self.parser.title) # find title and clean it

			# description :
			if self.parser.description == '':
				self.description = self.clean_text(self.parser.first_title)
			else:
				self.description = self.clean_text(self.parser.description)

			if self.parser.css:
				self.score += 0.5

			 # language :
			if self.parser.language != '':
				self.language = self.parser.language
				self.score += 0.5
			else:
				speak('No language : ' + self.url)

			# keywords :
			self.keywords = self.clean_keywords(self.parser.keywords) # get back keywords

			# links :
			if nofollow:
				self.links = list()
				speak('No take links')
			else:
				self.links = self.clean_links(self.parser.links)

			# favicon
			self.favicon = self.parser.favicon

			return (self.links, self.title, self.description, self.keywords,
				self.language, self.score, self.nb_words, self.favicon)
		else:
			return None, '', None, None, None, None, None, None

	def clean_text(self, text):
		"""Clean up text (\n\r\t )."""
		return ' '.join(text.split())

	def clean_links(self, links):
		"""Clean the list of links.

		new : the links to add in the new list of links

		"""
		links = list(set(links))
		new_list = list()
		canAdd = True

		for i, elt in enumerate(links):
			new = elt.strip()

			if new == '/' or new == '#' or new.startswith('mailto:') or 'javascript:' in new or new == '':
				continue
			else:
				if not new.startswith('http') and not new.startswith('www'):
					if new.startswith('/'):
						new = self.url + new
					elif new.startswith('//'):
						new = 'http' + new
					else:
						new = self.url + '/' + new

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

			if not new.endswith(tuple(BAD_EXTENTIONS)):
				new_list.append(new)

		return list(set(new_list))

	def clean_keywords(self, keywords):
		"""Clean found keywords."""
		if self.language == 'fr':
			stop_words = self.STOPWORDS['fr']
		elif self.language == 'en':
			stop_words = self.STOPWORDS['en']
		elif self.language == 'es':
			stop_words = self.STOPWORDS['es']
		elif self.language == 'it':
			stop_words = self.STOPWORDS['it']
		else:
			stop_words = []

		# size at the begining of the cleaning :
		keywords = keywords.lower().split() # str -> list

		begining = len(keywords) # stats

		result = []

		for keyword in keywords:
			# 2 chars at least and check if word is not only special chars
			if len(keyword) > 2 and not keyword.isnumeric():
				keyword = keyword.replace(' ', '')

				# remove useless chars
				if keyword.startswith(tuple(START_CHARS)):
					keyword = keyword[1:]

				if keyword.endswith(tuple(END_CHARS)):
					keyword = keyword[:-1]

				if len(keyword) > 1:
					if keyword[1] == '\'' or keyword[1] == '""':
						keyword = keyword[2:]

				# word/word2
				if '/' in keyword:
					keyword = keyword.split('/')

				if len(keyword) > 2:
					if isinstance(keyword, list):
						result.extend(keyword)
					else:
						result.append(keyword)

		self.nb_words = len(result)
		stats_stop_words(begining, self.nb_words)

		# after : (for test)
		with open('mot.txt', 'a', errors='replace') as myfile:
			myfile.write(str(result))
			myfile.write('\n\n')
		return result

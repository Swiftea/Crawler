#!/usr/bin/python3

"""Searches class :

MyParser is the html parser,
SiteInformations groups methodes for informations of the page.

"""

__author__ = "Seva Nathan"

from urllib.parse import urlparse


from package.data import * # to have required data
from package.module import speak, stats_stop_words, get_stopwords, clean_text, remove_duplicates
from package.parsers import MyParser

class SiteInformations:
	def __init__(self):
		"""Build the class : define variables."""
		self.url = str()
		self.score = float()
		self.title = str()
		self.description = str()
		self.language = str()
		self.links = list()
		self.images = list()
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
			self.title = clean_text(self.parser.title) # find title and clean it

			# description :
			if self.parser.description == '':
				self.description = clean_text(self.parser.first_title)
			else:
				self.description = clean_text(self.parser.description)

			if self.parser.css:
				self.score += 0.5

			 # language :
			if self.parser.language != '':
				self.language = self.parser.language
				self.score += 0.5
			else:
				speak('No language : ' + self.url)

			# keywords :
			keywords = clean_text(self.parser.keywords.lower()).split()
			begining_size = len(keywords) # stats
			self.keywords = self.clean_keywords(keywords)
			self.nb_words = len(self.keywords)
			stats_stop_words(begining_size, self.nb_words) # stats
			# tests :
			with open(DIR_OUTPUT + 'mot.txt', 'a', errors='replace') as myfile:
				myfile.write(str(self.keywords)) # problem !?)
				myfile.write('\n\n')

			# links :
			if nofollow:
				self.links = list()
				speak('No take links')
			else:
				self.links = self.clean_links(self.parser.links)

			# favicon :
			self.favicon = self.parser.favicon

			# images :
			self.images = list(set(self.clean_images(self.parser.images)))

			return (self.links, self.title, self.description, self.keywords,
				self.language, self.score, self.nb_words, self.favicon, self.images)
		else:
			return None, '', None, None, None, None, None, None, None

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
					infos_url = urlparse(self.url)
					base_url = infos_url.scheme + '://' + infos_url.netloc
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

	def clean_images(self, images):
		new_images = list()
		for key, image in enumerate(images):
			# image is a tuple : (url, alt)
			url = image[0].strip()

			if (url.endswith(IMG_EXTENTIONS) and
				not url.startswith('http') and
				not url.startswith('www')):
			
				if url.startswith('//'):
					url = 'http:' + url
				elif url.startswith('/'):
					url = self.url + url
				else:
					url = self.url + '/' + url
			if url.endswith('/'):
				url = url[:-1]
			slash = url.rfind('/')
			point = url.rfind('.')
			name = url[slash+1:point]

			new_images.append((url, image[1], name))
		return new_images

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

				if len(keyword) > 1: # l', d', s'
					if keyword[1] == '\'' or keyword[1] == '’':
						keyword = keyword[2:]
				if len(keyword) > 2:
					if keyword[-2] == '\'': # word's
						keyword = keyword[:-2]

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

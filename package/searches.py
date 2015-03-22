#!/usr/bin/python3

"""Searches class :

MyParser is the html parser,
SiteInformations groups methodes for informations of the page.

"""

__author__ = "Seva Nathan"

from urllib.parse import urlparse
from html.entities import *
from html.parser import HTMLParser


from package.data import * # to have required data
from package.module import speak, stats_stop_words, get_back_stopwords

class MyParser(HTMLParser):
	"""My parser for extract data.

	self.objet : the type of text for title, description and keywords
	dict(attrs).get('content') : convert attrs in a dict and retrun the value

	"""
	def __init__(self):
		HTMLParser.__init__(self)
		self.output_list = list() # list of links
		self.keywords = '' # all keywords in a string
		self.keyword_add = '' # the word to add to key
		self.objet = None
		self.css, self.h1 = False, False # if there is a css file in the source code
		self.first_title = '' # the first title (h1) of the web site
		self.description, self.language, self.title, self.favicon  = '', '', '', ''

	def handle_starttag(self, tag, attrs):
		if tag =='html': # bigining of the source code : reset all variables
			self.output_list = list()
			self.first_title, self.keywords, self.keyword_add = '', '', ''
			self.css, self.h1 = False, False
			self.description, self.language, self.title, self.favicon = '', '', '', ''
			self.objet = None

			if dict(attrs).get('lang') is not None:
				self.language = dict(attrs).get('lang').lower().strip()[:2]

		elif tag == 'a':
			url = dict(attrs).get('href')
			rel = dict(attrs).get('rel')
			if url is not None:
				if rel is not None:
					if 'noindex' not in rel:
						if 'nofollow' in rel:
							url += "!nofollow!"
							self.output_list.append(url)
						else:
							self.output_list.append(url)
				else:
					self.output_list.append(url)

		elif tag == 'title':
			self.objet = 'title' # il s'agit du titre

		elif tag == 'h1' and self.first_title == '':
			self.h1 = True # il s'agit d'un h1

		elif tag == 'link': # LINK REL="STYLESHEET" TYPE="text/css"
			if dict(attrs).get('rel') == 'stylesheet':
				self.css = True
				# LINK REL="ICON" HREF="FAVICON.ICO"
			elif dict(attrs).get('rel') == 'icon':
				if dict(attrs).get('href') is not None:
					self.favicon = dict(attrs).get('href')

		elif tag == "meta":
			name = dict(attrs).get('name')
			content = dict(attrs).get('content')
			if name is not None and content is not None:
				if name.lower() == 'description':
					self.description = content
					self.objet = 'description'
				elif name.lower() == 'language':
					self.language = content.lower().strip()[:2]

			httpequiv = dict(attrs).get('http-equiv')
			contentlanguage = dict(attrs).get('content-language')
			if httpequiv is not None and contentlanguage is not None:
				if httpequiv.lower() == 'content-language':
					self.language = contentlanguage.lower().strip()[:2]

		if (tag == 'h1' or tag == 'h2' or tag == 'h3' or tag == 'strong'
			or tag == 'em'):
			self.objet = 'key_word'

	def handle_data(self, data):
		if self.objet == 'title':
			self.title += data
		elif self.objet == 'key_word':
			self.keyword_add = self.keyword_add + ' ' + data
		if self.h1:
			self.first_title = data

	def handle_endtag(self, tag):
		if tag == 'title':
			self.objet = None
		elif (tag == 'h1' or tag == 'h2' or tag == 'h3'	or tag == 'strong'
			or tag == 'em'):
			self.objet = None
			self.keywords = self.keywords + ' ' + self.keyword_add
		elif tag == 'meta':
			self.objet = None
		if tag == 'h1':
			self.h1 = False

	def handle_entityref(self, name):
		try:
			letter = chr(name2codepoint[name])
		except KeyError:
			try:
				letter = html5[name + ';']
			except KeyError:
				speak('erreur handle_entityref', 11)
		else:
			if self.objet == 'title':
				self.add_letter(letter)

	def handle_charref(self, name):
		if name.startswith('x'):
			letter = chr(int(name[1:], 16))
		else:
			letter = chr(int(name))
		if self.objet == 'title':
			self.add_letter(letter)

	def add_letter(self, letter):
		self.title += letter


class Parser_encoding(HTMLParser):
	"""Searche encoding."""
	def __init__(self):
		HTMLParser.__init__(self)
		self.encoding = str()

	def handle_starttag(self, tag, attrs):
		if tag == "meta":
			# <meta charset="utf-8">
			charset = dict(attrs).get('charset')
			if charset is not None:
				self.encoding = charset

			# <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
			httpequiv = dict(attrs).get('http-equiv')
			content = dict(attrs).get('content')
			if httpequiv is not None and content is not None:
				if httpequiv.lower() == 'content-type':
					charset = content.find('charset')
					if charset != -1:
						self.encoding = content[charset+8:]


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

	def get_back_stopwords(self):
		self.STOP_WORDS = get_back_stopwords()
		if self.STOP_WORDS == dict():
			# no STOP_WORDS : the program will stop
			speak('pas de STOP_WORDS, le programme va se fermer')
			return 'error'
		else:
			return 'ok'

	def start_job(self, url, code, nofollow, score):
		"""Start all opérations.

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
				speak('pas de langue : ' + self.url)

			# key words :
			self.keywords = self.clean_keywords(self.parser.keywords) # get back keywords

			# links :
			if nofollow:
				self.links = list()
				speak('on ne prend pas les liens.')
			else:
				self.links = self.clean_links(self.parser.output_list)

			# favicon
			self.favicon = self.parser.favicon

			return (self.links, self.title, self.description, self.keywords,
				self.language, self.score, self.nb_words, self.favicon)
		else:
			return None, '', None, None, None, None, None

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

			if new == "/" or new == "#" or new[:7] == "mailto:" or 'javascript:' in new or new == '':
				continue
			else:
				# if the url need to be rebuild :
				if new[:4] != "http":
					if new[0] == "/": # if the url begin with /
						new = self.url + new
					else:
						new = self.url + "/" + new

				# delete anchors :
				infos_url = urlparse(new)
				new = infos_url.scheme + '://' + infos_url.netloc + infos_url.path

				if new.endswith('/'):
					new = new[:-1]

				nb_index = new.find("index.")
				if nb_index != -1:
					new = new[:nb_index]

				if infos_url.query != '':
					new += "?" + infos_url.query

			if not new.endswith(tuple(BAD_EXTENTIONS)):
				new_list.append(new)

		return list(set(new_list))

	def clean_keywords(self, keywords):
		"""Clean the keywords founded."""
		if self.language == 'fr':
			stop_words = self.STOP_WORDS['fr']
		elif self.language == 'en':
			stop_words = self.STOP_WORDS['en']
		elif self.language == 'es':
			stop_words = self.STOP_WORDS['es']
		elif self.language == 'it':
			stop_words = self.STOP_WORDS['it']
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

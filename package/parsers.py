#!/usr/bin/python3

"""Parsers using html.parser."""

from html.parser import HTMLParser
from html.entities import *


from package.module import speak

__author__ = "Seva Nathan"

class MyParser(HTMLParser):
	"""My parser for extract data.

	self.objet : the type of text for title, description and keywords
	dict(attrs).get('content') : convert attrs in a dict and retrun the value

	"""
	def __init__(self):
		HTMLParser.__init__(self)
		self.links = list() # list of links
		self.keywords = '' # all keywords in a string
		self.keyword_add = '' # the word to add to key
		self.objet = None
		self.css, self.h1 = False, False # if there is a css file in the source code
		self.first_title = '' # the first title (h1) of the web site
		self.description, self.language, self.title, self.favicon  = '', '', '', ''

	def handle_starttag(self, tag, attrs):
		if tag =='html': # bigining of the source code : reset all variables
			self.links = list()
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
							self.links.append(url)
						else:
							self.links.append(url)
				else:
					self.links.append(url)

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

		elif tag == 'meta':
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
				speak('error handle_entityref', 11)
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
		if tag == 'meta':
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

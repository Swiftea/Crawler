#!/usr/bin/python3

"""Data of webpage are geted by the python html.parser.
Here is two parser, the first one for all informations and
the sencond one only for encoding."""

from html.parser import HTMLParser
from html.entities import name2codepoint, html5

__author__ = "Seva Nathan"

class MyParser(HTMLParser):
	"""Html parser for extract data

	self.objet : the type of text for title, description and keywords
	dict(attrs).get('content') : convert attrs in a dict and retrun the value

	Data could be extract:
		title
		language
		description
		links with nofollow and noindex
		stylesheet
		favicon
		keywords: h1, h2, h3, strong, em

	"""
	def __init__(self):
		"""Build parser"""
		HTMLParser.__init__(self)
		self.links = list() # list of links
		self.keywords = '' # all keywords in a string
		self.objet = None # type of parsing information
		self.css = False # True if there is a css link in the source code
		self.h1 = False # True if parsing the title of webpage
		self.first_title = '' # the first title (h1) of the web site
		self.description = self.language = self.title = self.favicon  = ''

	def handle_starttag(self, tag, attrs):
		"""Call when parser met a starting tag

		:param tag: starting tag
		:type tag: str
		:param attrs: attributes: [('name', 'language'), ('content', 'fr')]
		:type attrs: list

		"""
		if tag =='html': # bigining of the source code : reset all variables
			self.links = list()
			self.first_title = self.keywords = self.description = ''
			self.language = self.title = self.favicon  = ''
			self.css = self.h1 = False
			self.objet = None

			if len(dict(attrs).get('lang', '')) >= 2:
				self.language = dict(attrs).get('lang').lower().strip()[:2]

		elif tag == 'a':
			url = dict(attrs).get('href')
			rel = dict(attrs).get('rel', '')
			if url:
				if 'noindex' not in rel:
					if 'nofollow' in rel:
						url += "!nofollow!"
						self.links.append(url)
					else:
						self.links.append(url)

		elif tag == 'title':
			self.objet = 'title' # it's about title

		elif tag == 'link': # LINK REL="STYLESHEET" TYPE="text/css"
			rel = dict(attrs).get('rel', '')
			if rel == 'stylesheet':
				self.css = True
				# LINK REL="ICON" HREF="FAVICON.ICO"
			elif rel == 'icon' or rel == 'shortcut icon':
				self.favicon = dict(attrs).get('href', '')

		elif tag == 'meta':
			language, description, objet = meta(attrs)
			if language != str():
				self.language = language
			if description != str():
				self.description = description
			if objet != str():
				self.objet = objet

		elif tag == 'h1' and self.first_title == '':
			self.h1 = True # it's about a h1

		if tag == 'h1' or tag == 'h2' or tag == 'h3' or tag == 'strong' or tag == 'em':
			self.objet = 'keyword'

	def handle_data(self, data):
		"""Call when parser met data

		:param tag: starting tag
		:type tag: str

		"""
		if self.objet == 'title':
			self.title += data
		elif self.objet == 'keyword':
			self.keywords += ' ' + data
		if self.h1:
			self.first_title = data

	def handle_endtag(self, tag):
		"""Call when parser met a ending tag

		:param tag: starting tag
		:type tag: str
		:param attrs: attributes
		:type attrs: list

		"""
		if tag == 'title':
			self.objet = None
		elif tag == 'h1' or tag == 'h2' or tag == 'h3'	or tag == 'strong' or tag == 'em':
			self.objet = None
		elif tag == 'meta':
			self.objet = None
		elif tag == 'p':
			self.text = False
		if tag == 'h1':
			self.h1 = False

	def handle_entityref(self, name):
		try:
			letter = chr(name2codepoint[name])
		except KeyError:
			try:
				letter = html5[name + ';']
			except KeyError:
				pass
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
		"""Add a letter to title when met special char"""
		self.title += letter

def meta(attrs):
	"""Manager searches in meat tag

	:apram attrs: attributes of meta tag
	:type attrs: list
	:return: language, description, objet

	"""
	objet = description = language = str()
	name = dict(attrs).get('name', '').lower()
	content = dict(attrs).get('content')
	if content:
		if name == 'description':
			description = content
			objet = 'description'
		elif name == 'language':
			language = content.lower().strip()[:2]

	httpequiv = dict(attrs).get('http-equiv')
	contentlanguage = dict(attrs).get('content')
	if httpequiv and contentlanguage:
		if httpequiv.lower() == 'content-language':
			language = contentlanguage.lower().strip()[:2]

	return language, description, objet

class Parser_encoding(HTMLParser):
	"""Html parser for extract encoding from source code"""
	def __init__(self):
		HTMLParser.__init__(self)
		self.encoding = str()

	def handle_starttag(self, tag, attrs):
		"""Call when parser met a starting tag

		:param tag: starting tag
		:type tag: str
		:param attrs: attributes
		:type attrs: list

		"""
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

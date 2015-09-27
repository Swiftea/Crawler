#!/usr/bin/python3

"""Define several functions SiteInformations."""

from urllib.parse import urlparse

from swiftea_bot.data import START_CHARS, END_CHARS, MIDLE_CHARS, ALPHABET, BAD_EXTENTIONS, DIR_DATA

def clean_text(text):
	"""Clean up text by removing tabulation, blank and carriage return.

	:param text: text to clean_text
	:type text: str
	:return: cleaned text

	"""
	return ' '.join(text.split())

def get_base_url(url):
	"""Get base url using urlparse.

	:param url: url
	:type url: str
	:return: base url of given url

	"""
	infos_url = urlparse(url)
	base_url = infos_url.scheme + '://' + infos_url.netloc
	return base_url

def remove_useless_chars(keyword):
	"""Remove useless chars in keyword.

	See data for all could be remove chars.
	Return None if keyword size is under two letters.

	:param keyword: keyword
	:type keyword: str
	:return: keyword or None

	"""
	while (keyword.startswith(START_CHARS) or keyword.endswith(END_CHARS) or keyword[1] == '\'' or
		keyword[1] == MIDLE_CHARS or keyword[-2] == '\'' or keyword[-2] == MIDLE_CHARS):

		if len(keyword) > 1:
			if keyword.startswith(START_CHARS):
				keyword = keyword[1:]
		else:
			return None
		if keyword.endswith(END_CHARS):
			keyword = keyword[:-1]
		if len(keyword) > 2:
			if keyword[1] == '\'' or keyword[1] == MIDLE_CHARS:
				keyword = keyword[2:]
		else:
			return None
		if len(keyword) > 2:
			if keyword[-2] == '\'' or keyword[-2] == MIDLE_CHARS:
				keyword = keyword[:-2]
		else:
			return None
		if len(keyword) <= 1:
			return None

	return keyword

def is_letters(keyword):
	"""Return True if one char at least is a letter.

	:param keyword: keyword to check
	:type keyword: str
	:return: True or False

	"""
	if True in [letter in ALPHABET for letter in keyword]:
		return True
	else:
		return False

def letter_repeat(keyword):
	"""Return True if the first letter isn't repeat eatch times."""
	if True not in [letter != '' for letter in keyword.split(keyword[0])]:
		return True  # '********'
	else:
		return False

def split_keywords(keyword):
	"""Split the given keyword by '.' and '/'.

	:param keyword: keyword to split
	:type keyword: str
	:return: True is the keyword was split and the list of new keyword or the keyword.

	"""
	is_list = False
	if '.' in keyword:
		keyword = keyword.split('.')
		is_list = True
	elif '/' in keyword:
		keyword = keyword.split('/')  # str -> list
		is_list = True
	elif '-' in keyword:
		keyword = keyword.split('-')  # str -> list
		is_list = True
	return is_list, keyword

def is_homepage(url):
	"""Check if url is the homepage.

	If there is only two '/' and two '.' if www and one otherwise.

	:param url: url to check
	:type url: str
	:return: True or False

	"""
	if url.count('/') == 2:
		if '//www.' in url and url.count('.') == 2:
			return True
		elif url.count('.') == 1:
			return True
		else:
			return False
	else:
		return False

def clean_link(url, base_url=None):
	"""Clean a link.

	Rebuild url with base url, pass mailto and javascript,
	remove anchors, pass if more than 5 query, pass if more than 255 chars,
	remove /index.xxx, remove last /.

	:param url: links to clean
	:type url: str
	:param base_url: base url for rebuilding, can be None if
	:return: cleaned link

	"""
	new = url.strip()  # Link to add in new list of links
	if (not new.endswith(BAD_EXTENTIONS) and
		new != '/' and
		new != '#' and
		not new.startswith('mailto:') and
		'javascript:' not in new and
		new != ''):
		if not new.startswith('http') and not new.startswith('www'):
			if new.startswith('//'):
				new = 'http:' + new
			elif new.startswith('/'):
				new = base_url + new
			elif new.startswith(':'):
				new = 'http' + new
			else:
				new = base_url + '/' + new
		infos_url = urlparse(new)  # Removing excpet ValueError
		new = infos_url.scheme + '://' + infos_url.netloc + infos_url.path
		if new.endswith('/'):
			new = new[:-1]
		nb_index = new.find('/index.')
		if nb_index != -1:
			new = new[:nb_index]
		if infos_url.query != '':
			new += '?' + infos_url.query

		if len(new) > 8 and new.count('&') < 5 and len(new) <= 255:
			return new
		else:
			return None
	else:
		return None

def capitalize(text):
	"""Upper the first letter of given text

	:param text: text
	:type text: str
	:return: text

	"""
	if len(text) > 0:
		return text[0].upper() + text[1:]
	else:
		return ''

def stats_stop_words(begining, end):
	"""Write the percentage of deleted word with stopwords for statistics.

	:param begining: size of keywords list before cleaning
	:type begining: int
	:param end: size of keywords list after cleaning
	:type end: int

	"""
	if begining != 0:
		stats = str(((begining - end) * 100) / begining)
	else:
		stats = '100'
	with open(DIR_DATA + 'stat_stopwords', 'a') as myfile:
		myfile.write(stats + '\n')

def stats_links(stats):
	"""Write the number of links for statistics.

	:param stat: number of list in a webpage
	:type stat: int

	"""
	with open(DIR_DATA + 'stat_links', 'a') as myfile:
		myfile.write(str(stats) + '\n')  # Write the number of links found

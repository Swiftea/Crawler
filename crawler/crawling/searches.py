#!/usr/bin/env python3

"""Define several functions SiteInformations."""


from urllib.parse import urlparse
from re import compile as compile_regex


from crawler.swiftea_bot.data import BAD_EXTENTIONS, DIR_STATS


regex = compile_regex(r'(\w+|\d+)')  # used in site_informations.py

def clean_text(text):
	"""Clean up text by removing tabulations, blanks and carriage returns.

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
	remove anchors, pass if more than 5 queries, pass if more than 255 chars,
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


def stats_links(stats):
	"""Write the number of links for statistics.

	:param stat: number of list in a webpage
	:type stat: int

	"""
	with open(DIR_STATS + 'stat_links', 'a') as myfile:
		myfile.write(str(stats) + '\n')  # Write the number of links found

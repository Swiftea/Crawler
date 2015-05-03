#!/usr/bin/python3

"""Define several functions for crawler"""

from urllib.parse import urlparse
from time import strftime
from os import path, mkdir, remove, listdir
import requests
import sys

import package.data as data

def tell(message, error_code=None, severity=1):
	"""Manage newspaper.

	Print in console that program doing and save a copy with time in event file.

	:param message: message to print and write
	:type message: str
	:param error_code: (optional) error code, if given call errors() with given message
	:type error_code: int
	:param severity: 1 is default severity, -1 add 4 spaces befor message,
		0 add 2 spaces befor the message, 2 uppercase and underline message.
	:type severity: int

	"""
	msg_to_print = message[:131]
	message = message.capitalize()
	if error_code:
		errors(message, error_code)
	else:
		error_code = ''

	if severity == -1:
		print('    ' + message[:127].lower())
	elif severity == 0:
		print('  ' + message[:129].lower())
	elif severity == 1:
		print(msg_to_print.capitalize())
	elif severity == 2:
		print(msg_to_print.upper())
		print(''.center(len(msg_to_print), '='))

	with open(data.FILE_NEWS, 'a') as myfile:
		myfile.write(strftime('%d/%m/%y %H:%M:%S') + str(error_code) + ' ' + message + '\n')

def errors(message, error_code):
	"""Write the error report with the time in errors file.

	Normaly call by tell() when a error_code parameter is given.

	:param message: message to print and write
	:type message: str
	:param error_code: error code
	:type error_code: int

	"""
	with open(data.FILE_ERROR, 'a') as myfile:
		myfile.write(str(error_code) + ' ' + strftime("%d/%m/%y %H:%M:%S") + ': ' + message + '\n')

def quit_program():
	"""Function who manage end of prgoram."""
	tell('end\n', 0)
	sys.exit()


def create_dirs():
	"""Manage crawler's runing.

	Test lot of things:
		create config directory\n
		create doc file if  doesn't exists\n
		create config file if it doesn't exists\n
		create links directory if it doesn't exists\n
		create index directory if it doesn't exists\n

	"""
	# Create directories if they don't exist:
	if not path.isdir(data.DIR_CONFIG):
		mkdir(data.DIR_CONFIG)
	if not path.isdir(data.DIR_DATA):
		mkdir(data.DIR_DATA)
	if not path.isdir(data.DIR_OUTPUT):
		mkdir(data.DIR_OUTPUT)
	if not path.isdir(data.DIR_INDEX):
		mkdir(data.DIR_INDEX)

def create_doc():
	"""Create doc file if it doesn't exist and if it was modified."""
	if not path.exists(data.FILE_DOC):
		with open(data.FILE_DOC, 'w') as myfile:
			myfile.write(data.ERROR_CODE_DOC)
	else:
		with open(data.FILE_DOC, 'r') as myfile:
			content = myfile.read()
		if content != data.ERROR_CODE_DOC:
			remove(data.FILE_DOC)
		with open(data.FILE_DOC, 'w') as myfile:
			myfile.write(data.ERROR_CODE_DOC)

def def_links():
	"""Create directory of links if it doesn't exist

	Ask to user what doing if there isn't basic links.
	Create a basic links file if user what it.

	"""
	if not path.isdir(data.DIR_LINKS):
		mkdir(data.DIR_LINKS)
		print("""No links directory,
1: let programm choose a list...
2: fill a file yourself...
(see doc.txt file in config)""")
		rep = input("What's your choice ? (1/2) : ")
		if rep == '1':
			# Basic links
			with open(data.FILE_BASELINKS, 'w') as myfile:
				myfile.write("""http://www.planet-libre.org
http://zestedesavoir.com
http://www.01net.com
https://www.youtube.com
http://www.lefigaro.fr
http://www.lemonde.fr
http://www.lepoint.fr
http://www.sport.fr
http://www.jeuxvideo.com
http://www.rueducommerce.fr
http://www.actu-environnement.com
https://fr.wikipedia.org
https://fr.news.yahoo.com
http://www.live.com
http://www.yahoo.com
http://www.lequipe.fr
http://swiftea.alwaysdata.net
http://trukastuss.over-blog.com""")
		elif rep == '2':
			open(data.FILE_BASELINKS, 'w').close()
			print("""
Create a file '0' without extention who contains a list of 20 links maximum.
They must start with 'http://' or 'https://' and no ends with '/'.
Choose popular websites.
Press enter when done.""")
			input()
		else:
			print('Please enter 1 or 2.')
			quit()

def is_index():
	"""Check if there is a saved inverted-index file.

	:return: True if there is one

	"""
	if path.exists(data.FILE_INDEX):
		return True
	else:
		return False

def dir_size(source):
	total_size = path.getsize(source)
	for item in listdir(source):
		itempath = path.join(source, item)
		if path.isfile(itempath):
			total_size += path.getsize(itempath)
		elif path.isdir(itempath):
			total_size += dir_size(itempath)
	return total_size


def average(content):  # Stats
	"""Calculate average.

	:param content: values
	:type content: list
	:return: average

	"""
	total = 0
	for value in content:
		total += float(value)
	moy = total / len(content)
	return moy

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
	with open(data.DIR_DATA + 'stat_stopwords', 'a') as myfile:
		myfile.write(stats + '\n')

def stats_links(stats):
	"""Write the number of links for statistics.

	:param stat: number of list in a webpage
	:type stat: int

	"""
	with open(data.DIR_DATA + 'stat_links', 'a') as myfile:
		myfile.write(str(stats) + '\n')  # Write the number of links found

def stats_webpages(begining, end):
	"""Write the time in second to crawl 10 webpages.

	:param begining: time before starting crawl 10 webpages
	:type begining: int
	:param end: time after crawled 10 webpages
	:type end: int

	"""
	delta = end - begining  # Time to crawl ten webpages
	time = delta / 10  # Time in second to crawl 10 webpages
	nb_webpages = 60 / time  # number of webpages crawled in 1 minute
	with open(data.DIR_DATA + 'stat_webpages', 'a') as myfile:
		myfile.write(str(nb_webpages) + '\n')

def stats_dl_index(begining, end):
	"""Write the time to download inverted-index.

	:param begining: time download inverted-index
	:type begining: int
	:param end: time after download inverted-index
	:type end: int

	"""
	with open(data.DIR_DATA + 'stat_dl_index', 'a') as myfile:
		myfile.write(str(end - begining) + '\n')

def stats_ul_index(begining, end):
	"""Write the time to upload inverted-index.

	:param begining: time before send inverted-index
	:type begining: int
	:param end: time after send inverted-index
	:type end: int

	"""
	with open(data.DIR_DATA + 'stat_up_index', 'a') as myfile:
		myfile.write(str(end - begining) + '\n')


def get_stopwords(path='http://swiftea.alwaysdata.net/data/stopwords/'):  # Search
	"""Get stopwords from swiftea website.

	:return: a dict: keys are languages and values are stopwords

	"""
	STOP_WORDS = dict()
	try:
		r = requests.get(path + 'fr.stopwords.txt')
		r.encoding = 'utf-8'
		STOP_WORDS['fr'] = r.text
		r = requests.get(path + 'en.stopwords.txt')
		r.encoding = 'utf-8'
		STOP_WORDS['en'] = r.text
	except requests.exceptions.ConnectionError:
		print('Failed to get stopwords', 10)
		return None
	else:
		return STOP_WORDS


def clean_text(text):  # Search
	"""Clean up text by removing tabulation, blank and carriage return.

	:param text: text to clean_text
	:type text: str
	:return: cleaned text

	"""
	return ' '.join(text.split())

def remove_duplicates(old_list):  # Search
	"""Remove duplicates from a list.

	:param old_list: list to clean
	:type old_list: list
	:return: list without duplicates

	"""
	new_list = list()
	for elt in old_list:
		if elt not in new_list:
			new_list.append(elt)
	return new_list

def get_base_url(url):  # Search
	"""Get base url using urlparse.

	:param url: url
	:type url: str
	:return: base url of given url

	"""
	infos_url = urlparse(url)
	base_url = infos_url.scheme + '://' + infos_url.netloc
	return base_url

def check_size_keyword(keyword):  # Search
	"""Return True if size of given keyword is over than 2."""
	if len(keyword) > 2:
		return True
	else:
		return False

def remove_useless_chars(keyword):  # Search
	"""Remove useless chars in keyword.

	See data for all could be remove chars.
	Return None if keyword size is under two letters.

	:param keyword: keyword
	:type keyword: str
	:return: keyword or None

	"""
	while (keyword.startswith(data.START_CHARS) or keyword.endswith(data.END_CHARS) or keyword[1] == '\'' or
		keyword[1] == data.MIDLE_CHARS or keyword[-2] == '\'' or keyword[-2] == data.MIDLE_CHARS):
		if keyword.startswith(data.START_CHARS):
			keyword = keyword[1:]
		if keyword.endswith(data.END_CHARS):
			keyword = keyword[:-1]
		if check_size_keyword(keyword):
			if keyword[1] == '\'' or keyword[1] == data.MIDLE_CHARS:
				keyword = keyword[2:]
		if check_size_keyword(keyword):
			if keyword[-2] == '\'' or keyword[-2] == data.MIDLE_CHARS:
				keyword = keyword[:-2]
		else:
			return None

	if check_size_keyword(keyword):
		return keyword
	else:
		return None

def is_letters(keyword):  # Search
	"""Return True if one char at least is a letter.

	:param keyword: keyword to check
	:type keyword: str
	:return: True or False

	"""
	if True in [letter in data.ALPHABET for letter in keyword]:
		return True
	else:
		return False

def letter_repeat(keyword):  # Search
	"""Return True if the first letter isn't repeat eatch times."""
	if True not in [letter != '' for letter in keyword.split(keyword[0])]:
		return True  # '********'
	else:
		return False

def split_keywords(keyword):  # Search
	"""Split the given keyword by '.' and '/'.

	:param keyword: keyword to split
	:type keyword: str
	:return: True is the keyword was split and the list of new keyword or the keyword.

	"""
	is_list = False
	if '.' in keyword:
		keyword = keyword.split('.')
		is_list = True
	if '/' in keyword:
		keyword = keyword.split('/')  # str -> list
		is_list = True
	return is_list, keyword

def is_homepage(url):  # Search
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
	if (not new.endswith(data.BAD_EXTENTIONS) and
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
		infos_url = urlparse(new)
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


def meta(attrs):  # Parser
	"""Manager searches in meat tag.

	Can find:
		<meta name='description' content='my description'/>\n
		<meta name='language' content='en'/>\n
		<meta http-equiv='content-language' content='en'/>\n

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

def can_append(url, rel):  # Parser
	"""Check rel attrs to know if crawler can take this the link.

	Add !nofollow! at the end of the url if can't follow links of url.

	:param url: url to add
	:type url: str
	:param rel: rel attrs in a tag
	:type rel: str
	:return: None if can't add it, otherwise return url

	"""
	if url:
		if 'noindex' not in rel:
			if 'nofollow' in rel:
				url += '!nofollow!'
			return url
		else:
			return None
	else:
		return None


def convert_keys(inverted_index):  # Inverted-index
	"""Convert str words keys into int from inverted-index.

	Json convert doc id key in str, must convert in int.

	:param inverted_index: inverted_index to convert
	:tyep inverted_index: dict
	:return: converted inverted-index

	"""
	new_inverted_index = dict()
	for language in inverted_index:
		new_inverted_index[language] = dict()
		for first_letter in inverted_index[language]:
			new_inverted_index[language][first_letter] = dict()
			for two_letter in inverted_index[language][first_letter]:
				new_inverted_index[language][first_letter][two_letter] = dict()
				for word in inverted_index[language][first_letter][two_letter]:
					new_inverted_index[language][first_letter][two_letter][word] = dict()
					for doc_id in inverted_index[language][first_letter][two_letter][word]:
						new_inverted_index[language][first_letter][two_letter][word][int(doc_id)] = inverted_index[language][first_letter][two_letter][word][doc_id]
	return new_inverted_index


def no_connexion(url='http://swiftea.alwaysdata.net'):  # Web connexion
	"""Check connexion.

	Try to connect to swiftea website.

	:param url: url use by test
	:return: True if no connexion

	"""
	try:
		requests.get(url)
	except requests.exceptions.RequestException:
		tell('No connexion')
		return True
	else:
		return False

def is_nofollow(url):  # Web connexion
	"""Check if take links.

	Search !nofollow! at the end of url, remove it if found.

	:param url: webpage url
	:type url: str
	:return: True if nofollow and url

	"""
	if url.endswith('!nofollow!'):
		return True, url[:-10]
	else:
		return False, url

def url_is_secure(url):  # Web connexion
	"""Check if given url is secure (https).

	:param url: url to check
	:type url: str
	:return: True if url is secure

	"""
	if url.startswith('https'):
		return True
	else:
		return False

def convert_secure(url):  # Web connexion
	"""Convert https to http and http to https.

	:param url: url to convert
	:type url: str
	:return: converted url

	"""
	if url_is_secure(url):
		return url[:4] + url [5:]
	else:
		return url[:4] + 's' + url [4:]

#!/usr/bin/python3

"""Define several functions for crawler"""

from time import strftime
from os import path, mkdir, remove, listdir
import requests
from urllib.parse import urlparse
import sys

import package.data as data

def speak(message, EC=None):
	"""Manage newspaper.

	This function print in console that program doing and save a copy in
	event file.

	:param message: message to print and write
	:type message: str
	:param EC: (optional) error code, if given call errors() with given message
	:type EC: int
	"""
	if EC:
		print(str(EC) + ' ' + message)
		with open(data.FILE_NEWS, 'a') as myfile:
			myfile.write(str(EC) + ' ' + message + '\n')
		errors(EC, message)
	else:
		print(message)
		with open(data.FILE_NEWS, 'a') as myfile:
			myfile.write(message + '\n')

def errors(EC, message):
	"""Write the error report with time in errors file.

	Normaly call by speak() when a EC parameter is given

	:param message: message to print and write
	:type message: str
	:param EC: error code
	:type EC: int
	"""
	with open(data.FILE_ERROR, 'a') as myfile:
		myfile.write(str(EC) + ' ' + strftime("%d/%m/%y %H:%M:%S") + ' : ' + message + '\n')

def quit_program():
	"""Function who manage end of prgoram.

	Call speak() with 'end' and exit
	"""
	speak('end\n', 0)
	sys.exit()


def create_dirs():
	"""Manage crawler's runing.

	Test lot of things :
		create config directory
		create doc file if  doesn't exists
		create config file if it doesn't exists
		create links directory if it doesn't exists
		create index directory if it doesn't exists
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
	"""Create doc file if it doesn't exist."""
	if not path.exists(data.FILE_DOC):
		with open(data.FILE_DOC, 'w') as myfile:
			myfile.write(data.README)
	else:
		with open(data.FILE_DOC, 'r') as myfile:
			content = myfile.read()
		if content != data.README:
			remove(data.FILE_DOC)
		with open(data.FILE_DOC, 'w') as myfile:
			myfile.write(data.README)


def def_links():
	"""Create directory of links if it doesn't exist."""
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

	:return: True if there is the file
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


def stats_stop_words(begining, end):
	"""Percentage of deleted word with stopwords for statistics.

	Write the percentage in stats file.

	:param begining: size of keywords list before cleaning
	:type begining: int
	:param end: size of keywords list after cleaning
	:type end: int
	"""
	if end != 0:
		stats = str(((begining-end) * 100) / end)
	else:
		stats = '0'
	with open(data.FILE_STATS2, 'a') as myfile:
		myfile.write(stats + '\n')

def stats_links(stat):
	"""Write the number of links for statistics in stats file.

	:param stat: number of list in a webpage
	:type stat: int
	"""
	with open(data.FILE_STATS, 'a') as myfile:
		myfile.write(str(stat) + '\n')  # Write the number of links found

def average(content=list):  # Stats
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
	"""Clean up text (\\n\\r\\t).

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
	if True not in [letter in keyword for letter in data.ALPHABET]:
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
	is_list = False
	if '.' in keyword:
		keyword = keyword.split('.')
		is_list = True
	if '/' in keyword:
		keyword = keyword.split('/')  # str -> list
		is_list = True
	return is_list, keyword

def is_homepage(url):  # Search
	"""Check if url is the homepage

	:param url: url to check
	:type url: str
	:return: true or false
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


def meta(attrs):  # Parser
	"""Manager searches in meat tag.

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
	"""Check rel attrs.

	:param url: url to add
	:type url: str
	:param rel: rel attrs in a tag
	:type rel: str
	:return: url or None if can't add it
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


def rebuild_links(old_links, new_links):  # File manager
	"""Rebuild list of links.

	:param old_links: links already in file
	:type old_links: list
	:param new_links: links to add
	:type new_links: list
	:return: links to write in file
	"""
	links = old_links + new_links
	links_to_add = list()
	for link in links:
		if link not in links_to_add and len(link) <= 255:
			links_to_add.append(link)
	return links_to_add


def convert_keys(inverted_index):  # Inverted-index
	"""Convert str words keys into int from inverted-index.

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

	:param url: url use by test
	:return: True if no connexion
	"""
	try:
		requests.get(url)
	except requests.exceptions.RequestException:
		speak('No connexion')
		return True
	else:
		return False

def is_nofollow(url):  # Web connexion
	"""Check if take links.

	:param url: webpage url
	:type url: str
	:return: true if nofollow and url
	"""
	if url.endswith('!nofollow!'):
		return True, url[:-10]
	else:
		return False, url

def url_is_secure(url):  # Web connexion
	"""Check if given url is secure (https).

	:param url: url to check
	:type url: str
	:return: true if secure
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

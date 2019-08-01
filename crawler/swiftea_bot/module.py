#!/usr/bin/env python3

"""Define several functions for all crawler's class."""

from time import strftime
from os import path, mkdir, listdir
import sys
import json


import crawler.swiftea_bot.data as data
from crawler.swiftea_bot import links


def tell(message, error_code='', severity=1):
	"""Manage newspaper.

	Print in console what the program is doing and save this in a copy with time in an event file.

	:param message: message to print and write
	:type message: str
	:param error_code: (optional) error code, if given call errors() with given message
	:type error_code: int
	:param severity: 1 is default severity, -1 add 4 spaces befor message,
		0 add 2 spaces befor the message, 2 uppercase and underline message.
	:type severity: int

	"""
	msg_to_print = message[:132]
	message = message.capitalize()
	if error_code != '':
		errors(message, error_code)

	if severity == -1:
		print('    ' + message[:127].lower())
	elif severity == 0:
		print('  ' + message[:129].lower())
	elif severity == 1:
		print(msg_to_print.capitalize())
	elif severity == 2:
		print(msg_to_print.upper())
		print(''.center(len(msg_to_print), '='))

	with open(data.FILE_EVENTS, 'a') as myfile:
		myfile.write(strftime('%d/%m/%y %H:%M:%S') + str(error_code) + ' ' + message + '\n')

def safe_quit():
	tell('exiting', 0, 2)
	sys.exit(1)

def errors(message, error_code):
	"""Write the error report with the time in errors file.

	Normaly call by tell() when a error_code parameter is given.

	:param message: message to print and write
	:type message: str
	:param error_code: error code
	:type error_code: int

	"""
	with open(data.FILE_ERRORS, 'a') as myfile:
		myfile.write(' ' + str(error_code) + ' ' + strftime("%d/%m/%y %H:%M:%S") + ': ' + message + '\n')


def create_dirs():
	"""Manage crawler's running.

	Test a lot of things:
		create config directory\n
		create doc file if  doesn't exists\n
		create config file if it doesn't exists\n
		create links directory if it doesn't exists\n
		create index directory if it doesn't exists\n

	"""
	# Create directories if they don't exist:
	if not path.isdir(data.DIR_CONFIG):
		mkdir(data.DIR_CONFIG)
	if not path.isdir(data.DIR_INDEX):
		mkdir(data.DIR_INDEX)
	if not path.isdir(data.DIR_STATS):
		mkdir(data.DIR_STATS)
	if not path.isdir(data.DIR_LINKS):
		mkdir(data.DIR_LINKS)


def def_links():
	"""Create directory of links if it doesn't exist
	Ask to user what doing if there isn't basic links.
	Create a basic links file if user what it.
	"""
	if len(listdir(data.DIR_LINKS)) == 0:
		print("""No links file to start crawling:
1: let the crawler uses it default list
2: fill a file yourself""")
		rep = ''
		while rep not in ('1', '2'):
			rep = input("What's your choice? (1/2): ")

		if rep == '1':
			# Basic links
			with open(data.FILE_BASELINKS, 'w') as myfile:
				myfile.write(data.BASE_LINKS)
		elif rep == '2':
			open(data.FILE_BASELINKS, 'w').close()
			print("""Create a file called "0" in the "data/links" directory that contains a list of 20 links maximum.
They must start with "http://" or "https://" and not end with a "/".
Press enter when done.""")
			input()


def is_index():
	"""Check if there is a saved inverted-index file.

	:return: True if there is one

	"""
	if path.exists(data.FILE_INDEX):
		return True
	else:
		return False


def can_add_doc(docs, new_doc):
	"""To avoid documents duplicate, look for all url doc.

	Parse self.infos of Crawler and return True if new_doc isn't in it.

	:param docs: the documents to check
	:type docs: list
	:param new_doc: the doc to add
	:type new_doc: dict
	:return: True if can add the doc

	"""
	for doc in docs:
		if doc['url'] == new_doc['url']:
			return False
	return True


def remove_duplicates(old_list):
	"""Remove duplicates from a list, keeps order.

	:param old_list: list to clean
	:type old_list: list
	:return: list without duplicates

	"""
	new_list = list()
	for elt in old_list:
		if elt not in new_list:
			new_list.append(elt)
	return new_list


def stats_webpages(begining, end):
	"""Write the time in second to crawl 10 webpages.

	:param begining: time before starting crawl 10 webpages
	:type begining: int
	:param end: time after crawled 10 webpages
	:type end: int

	"""
	delta = end - begining  # Time to crawl ten webpages
	time = delta / 10  # Time in second to crawl n webpages
	nb_webpages = 60 / time  # Number of webpages crawled in 1 minute
	with open(data.DIR_STATS + 'stat_webpages', 'a') as myfile:
		myfile.write(str(nb_webpages) + '\n')


def stats_send_index(begining, end):
	"""Time spent between two sending of index"""
	with open(data.DIR_STATS + 'stats_send_index', 'a') as myfile:
		myfile.write(str(end - begining) + '\n')


def convert_keys(inverted_index):
	"""Convert `str` words keys into `int` from inverted-index.

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

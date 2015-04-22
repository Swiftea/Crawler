#!/usr/bin/python3

"""Define several functions for crawler"""

__author__ = "Seva Nathan"

from sys import exit # to leave the programme
from time import strftime # to have date and time data
from os import path, mkdir, remove
import requests
from urllib.parse import urlparse


import package.data as data

def speak(message, EC=None):
	"""Manage newspaper

	This function print in console that program doing and save a copy in
	newspaper file

	:param message: message to print and write
	:type message: str
	:param EC: (optional) error code, if given call errors() with given message
	:type EC: int

	"""
	if EC:
		print(str(data.EC) + ' ' + message)
		with open(data.FILE_NEWS, 'a') as myfile:
			myfile.write(str(data.EC) + ' ' + message + '\n')
		errors(EC, message)
	else:
		print(message)
		with open(data.FILE_NEWS, 'a') as myfile:
			myfile.write(message.capitalize() + '\n')

def errors(EC, message):
	"""Write the error report with time in errors file

	Normaly call by speak() when a EC parameter is given

	:param message: message to print and write
	:type message: str
	:param EC: error code
	:type EC: int

	"""
	with open(data.FILE_ERROR, 'a') as myfile:
		myfile.write(str(data.EC) + ' ' + strftime("%d/%m/%y %H:%M:%S") + ' : ' + message + '\n')

def quit():
	"""Function who manage end of prgoram

	Call speak() with 'end' and exit

	"""
	speak('end\n', 0)
	exit()

def clean_text(text):
	"""Clean up text (\\n\\r\\t)

	:param text: text to clean_text
	:type text: str
	:return: cleaned text

	"""
	return ' '.join(text.split())

def remove_duplicates(old_list):
	"""remove duplicates from a list

	:param old_list: list to clean
	:type old_list: list
	:return: list without duplicates

	"""
	new_list = list()
	for elt in old_list:
		if elt not in new_list:
			new_list.append(elt)
	return new_list

def stats_stop_words(begining, end):
	"""Percentage of deleted word with stopwords for statistics

	:param begining: size of keywords list before cleaning
	:type begining: int
	:param end: size of keywords list after cleaning
	:type end: int

	"""
	if end != 0:
		stats = str(((begining-end) * 100) / end)
	else:
		stats = 0
	with open(data.FILE_STATS2, 'a') as myfile:
		myfile.write(str(stats) + '\n')

def stats_links(stat):
	"""Number of links for statistics

	:param stat: number of list in a webpage
	:type stat: int

	"""
	with open(data.FILE_STATS, 'a') as myfile:
		myfile.write(stat + '\n') # write the number of links found

def start():
	"""Manage crawler's runing

	Test lot of things :
		create config directory
		create doc file if  doesn't exists
		create config file if it doesn't exists
		create links directory if it doesn't exists
		create index directory if it doesn't exists

	"""
	# create directories if they don't exist
	if not path.isdir(data.DIR_CONFIG):
		mkdir(data.DIR_CONFIG)
	if not path.isdir(data.DIR_DATA):
		mkdir(data.DIR_DATA)
	if not path.isdir(data.DIR_OUTPUT):
		mkdir(data.DIR_OUTPUT)
	if not path.isdir(data.DIR_INDEX):
		mkdir(data.DIR_INDEX)

	# create doc file if it doesn't exist :
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

	# create directory of links if it doesn't exist :
	if not path.isdir(data.DIR_LINKS):
		print("""No links directory,
1: let programm choose a list...
2: fill a file yourself...
(see doc.txt file in config)""")
		rep = input("What's your choice ? (1/2) : ")
		if rep == '1':
			# basic links
			mkdir(data.DIR_LINKS)
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
			mkdir(data.DIR_LINKS)
			open(data.FILE_BASELINKS, 'x').close()
			print("""
Create a file '0' without extention who contains a list of 20 links maximum.
They must start with 'http://' or 'https://' and no ends with '/'.
Choose popular websites.
Press enter when done.""")
			input()

		else:
			print('Please enter 1 or 2.')
			quit()

def get_stopwords():
	"""Get stopwords from swiftea website

	:return: a dict: keys are languages and values are stopwords

	"""
	STOP_WORDS = dict()
	try:
		r = requests.get('http://swiftea.alwaysdata.net/data/stopwords/fr.stopwords.txt')
		r.encoding = 'utf-8'
		STOP_WORDS['fr'] = r.text
		r = requests.get('http://swiftea.alwaysdata.net/data/stopwords/en.stopwords.txt')
		r.encoding = 'utf-8'
		STOP_WORDS['en'] = r.text
	except requests.exceptions.ConnectionError:
		print('Failed to get stopwords', 10)
		return None
	else:
		return STOP_WORDS

def get_base_url(url):
	"""Get base url using urlparse

	:param url: url
	:type url: str
	:return: base url of given url

	"""
	infos_url = urlparse(url)
	base_url = infos_url.scheme + '://' + infos_url.netloc
	return base_url

def no_connexion():
	"""Check connexion

	:return: True if no connexion

	"""
	try:
		requests.get('http://swiftea.alwaysdata.net/')
	except requests.exceptions.RequestException:
		speak('No connexion')
		return True
	else:
		return False

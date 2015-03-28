#!/usr/bin/python3

"""Define functions and create files and directories for user and program."""

__author__ = "Seva Nathan"

from sys import exit # to leave the programme
from time import strftime # to have date and time data
from os import path, mkdir, remove
import requests # to get back stopwords


from package.data import * # to get required data

def speak(message, EC=None):
	"""Manage the newspaper.

	print() and write() message.
	This function print in console that the program do and save a copy in the
	newspaper file.
	EC : error code : optional, if given run errors function

	"""
	if EC:
		print(str(EC) + ' ' + message)
		with open(FILE_NEWS, 'a') as myfile:
			myfile.write(str(EC) + ' ' + message + '\n')
		errors(EC, message)
	else:
		print(message)
		with open(FILE_NEWS, 'a') as myfile:
			myfile.write(message.capitalize() + '\n')

def errors(EC, message):
	"""Write the error report in the errors file.

	Normaly call by speak function when a EC parameter is given.
	EC : error code

	"""
	with open(FILE_ERROR, 'a') as myfile:
		myfile.write(str(EC) + ' ' + strftime("%d/%m/%y %H:%M:%S") + ' : ' + message + '\n')

def quit():
	"""Function who manage the end of the prgoram."""
	speak('end\n', 0)
	exit()

def clean_text(text):
	"""Clean up text (\n\r\t )."""
	return ' '.join(text.split())

def stats_stop_words(begining, end):
	"""Percentage of deleted word with stopwords for statistics."""
	if end != 0:
		stats = str(((begining-end) * 100) / end)
	else:
		stats = 0
	with open(FILE_STATS2, 'a') as myfile:
		myfile.write(str(stats) + '\n')

def stats_links(stat):
	"""Number of links for statistics."""
	with open(FILE_STATS, 'a') as myfile:
		myfile.write(stat + '\n') # write the number of links found

def start():
	"""Test lot off things :

	create config derectory
	create doc file if it doesn't exist
	create config file if it doesn't exist
	create links directory if it doesn't exist
	create index directory if it doesn't exist

	"""
	# create directories if they don't exist
	if not path.isdir(DIR_CONFIG):
		mkdir(DIR_CONFIG)
	if not path.isdir(DIR_DATA):
		mkdir(DIR_DATA)
	if not path.isdir(DIR_OUTPUT):
		mkdir(DIR_OUTPUT)

	# create doc file if it doesn't exist :
	if not path.exists(FILE_DOC):
		with open(FILE_DOC, 'w') as myfile:
			myfile.write(README)
	else:
		with open(FILE_DOC, 'r') as myfile:
			content = myfile.read()
		if content != README:
			remove(FILE_DOC)
		with open(FILE_DOC, 'w') as myfile:
			myfile.write(README)

	# create directory of links if it doesn't exist :
	if not path.isdir(DIR_LINKS):
		print("""No links directory,
1: let programm choose a list...
2: fill a file yourself...
(see doc.txt file in config)""")
		rep = input("What's your choice ? (1/2) : ")
		if rep == '1':
			# basic links
			mkdir(DIR_LINKS)
			with open(FILE_BASELINKS, 'w') as myfile:
				myfile.write("""http://www.planet-libre.org
http://www.jeux.fr
http://fr.openclassrooms.com
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
		else:
			print("""
Create a file '0' without extention who contains a list of 20 links maximum.
They must start with 'http://' or 'https://' and no ends with '/'.
Choose popular websites.
Press enter when done""")
			input()

def get_stopwords():
	STOP_WORDS = dict()
	try:
		r = requests.get('http://swiftea.alwaysdata.net/data/stopwords/fr.stopwords.txt')
		r.encoding = 'utf-8'
		STOP_WORDS['fr'] = r.text
		r = requests.get('http://swiftea.alwaysdata.net/data/stopwords/en.stopwords.txt')
		r.encoding = 'utf-8'
		STOP_WORDS['en'] = r.text
		r = requests.get('http://swiftea.alwaysdata.net/data/stopwords/es.stopwords.txt')
		r.encoding = 'utf-8'
		STOP_WORDS['es'] = r.text
		r = requests.get('http://swiftea.alwaysdata.net/data/stopwords/it.stopwords.txt')
		r.encoding = 'utf-8'
		STOP_WORDS['it'] = r.text
	except requests.exceptions.ConnectionError:
		print('Failed to get stopwords', 10)
		return dict()
	else:
		return STOP_WORDS

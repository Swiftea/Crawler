#!/usr/bin/python3

"""Display stats"""

from os import system

from package.data import *

__author__ = "Seva Nathan"

def average(content=list):
	"""Calculate average

	:param content: values
	:type content: list
	:return: average

	"""
	total = 0
	for value in content:
	    total += int(value)
	moy = total / len(content)
	return moy

if __name__ == '__main__':
	try:
		with open(FILE_STATS, 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:
		print('File ' + FILE_STATS + ' not found.')
	else:
		moy = average(content)
		print('Average percentage of removed words : ' + str(moy))
	try:
		with open(FILE_STATS2, 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:
		print('File ' +  FILE_STATS2 + ' not found.')
	else:
		moy = average(content)
		print('Average links in webpage : ' + str(moy))

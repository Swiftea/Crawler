#!/usr/bin/python3

"""Display stats"""

from package.data import FILE_STATS, FILE_STATS2
from package.module import average

__author__ = "Seva Nathan"

if __name__ == '__main__':
	try:
		with open(FILE_STATS, 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:
		print('File ' + FILE_STATS + ' not found.')
	else:
		print('Average percentage of removed words : ' + str(average(content)))
	try:
		with open(FILE_STATS2, 'r') as myfile:
			content = myfile.read().split()
	except FileNotFoundError:
		print('File ' +  FILE_STATS2 + ' not found.')
	else:
		print('Average links in webpage : ' + str(average(content)))

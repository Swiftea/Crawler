#!/usr/bin/python3

"""testeur de fonction crawler"""

from os import system

from package.data import *

__author__ = "Seva Nathan"


def stats_links():
	try: fichier = open(FILE_STATS, 'r')
	except FileNotFoundError:
		print("File stats.txt not found")
		return None
	contenu = fichier.read()
	fichier.close()
	liste = contenu.split()
	total = 0
	for i, elt in enumerate(liste):
	    total += int(elt)
	moy = total / len(liste)
	print('Average links in webpage : ' + str(moy))
	return None

def stats_keywords():
	try: fichier = open(FILE_STATS2, 'r')
	except FileNotFoundError:
		print("File stats2.txt not found")
		return None
	else:
		contenu = fichier.read()
		fichier.close()
		liste = contenu.split()
		total = 0
		for i, elt in enumerate(liste):
			total += float(elt)
		moy = total / len(liste)
		print('Average percentage of removed words : ' + str(moy))
	return None

if __name__ == '__main__':
	stats_links()
	stats_keywords()
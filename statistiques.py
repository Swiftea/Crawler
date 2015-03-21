#!/usr/bin/python
# -*-coding:Utf-8 -*

"""testeur de fonction crawler"""

from os import system

from package.data import *

__author__ = "Seva Nathan"


def stats_links():
	try: fichier = open(FILE_STATS, 'r')
	except FileNotFoundError:
		print("fichier stats.txt introuvable")
		return None
	contenu = fichier.read()
	fichier.close()
	liste = contenu.split()
	total = 0
	for i, elt in enumerate(liste):
	    total += int(elt)
	moy = total / len(liste)
	print('moyenne de liens dans une url : ' + str(moy))
	return None

def stats_keywords():

	try: fichier = open(FILE_STATS2, 'r')
	except FileNotFoundError:
		print("fichier stats2.txt introuvable")
		return None
	else:
		contenu = fichier.read()
		fichier.close()
		liste = contenu.split()
		total = 0
		for i, elt in enumerate(liste):
			total += float(elt)
		moy = total / len(liste)
		print('moyenne des pourcentages de mot supprimé : ' + str(moy))
	return None

if __name__ == '__main__':
	stats_links()
	stats_keywords()
	system('pause')

#!/usr/bin/python

"""Crawler5 for Swiftea : http://swiftea.alwaysdata.net"""

from os import system
from time import strftime


from package.module import speak, leaving, start
from package.data import *
from package.web_connexion import WebConnexion
from package.file_management import FileManagement
from package.database_swiftea import DataBase_swiftea
from package.searches import SiteInformations
from package.inverted_index import InvertedIndex
from package.FTP_swiftea import FTPSwiftea

__author__ = "Seva Nathan"

class Crawler6:
	"""Crawler Class.

	rep : a message
	result : data asked

	"""
	def __init__(self):
		start()
		self.web_site_infos = SiteInformations()
		if self.web_site_infos.get_back_stopwords() is 'error':
			leaving()
		self.file_management = FileManagement()
		self.ftp = FTPSwiftea(HOST_FTP, USER, PASSWORD)
		self.inverted_index = InvertedIndex()
		result, rep = self.ftp.get_index(FILE_INDEX, FTP_INDEX)
		if result is None and self.file_management.reading_file_number != 0:
			speak("pas d'index, le programme va se fermer")
			leaving()
		else:
			self.inverted_index.setIndex(result)
		self.inverted_index.setSTOP_WORDS(self.web_site_infos.STOP_WORDS)
		self.data_base = DataBase_swiftea(HOST_DB, USER, PASSWORD, NAME_DB)
		self.webconnexion = WebConnexion()

		self.infos, self.links = list(), list()

	def start(self):
		nbr_page_crawl = 0
		speak(strftime("%d/%m/%y %H:%M:%S")) # speak time
		while True:
			for k in range(3):
				while len(self.infos) < 10:
					# speak what is happen:
					speak('lecture : {0}, liens : {1}'.format(
						str(self.file_management.reading_file_number),
						str(self.file_management.reading_line_number+1)))
					# get the url of the web site :
					url = self.file_management.get_url()
					if url is 'continue': # if there is an error
						continue # redémare la boucle
					elif url is 'stop':
						self.end()
					self.crawl_web_site(url)
					self.file_management.save_links(list(set(self.links)))

				# end of crawling loop

				nbr_page_crawl += 10
				speak('{} nouveaux documents ! '.format(nbr_page_crawl))

				self.send_DB()
				self.indexation()
				# reset the list of dict of informations of webs sites : 
				self.infos.clear()
				# get_nbr_max, save_meters, get_stop, check_size_file : 
				self.file_management.sometimes()
				# user wants stop ? :
				if self.file_management.run is False:
					speak('the user want stop program')
					self.end()

			# end of loop range(3) : 30 web sites crawling

			self.send_index()
			self.suggestions()

	def crawl_web_site(self, url):
		"""score : .5 encodage, .5 css, .5 langue, """
		speak('url : ' + url) # speak the url
		# get the code of web page : 
		code, nofollow, score = self.webconnexion.get_code(url)
		if code is 'continue':
			return
		infoswebpage = {}
		infoswebpage['url'] = url
		(links, infoswebpage['title'], infoswebpage['description'],
			infoswebpage['keywords'], infoswebpage['language'],
			infoswebpage['score'], infoswebpage['nb_words']
			) = self.web_site_infos.start_job(url, code, nofollow, score)
		if infoswebpage['title'] is '':
			return
		else:
			self.infos.append(infoswebpage)
			self.links.extend(links)

	def send_DB(self):
		# can_send = self.ftp.can_send()
		rep = self.data_base.send_infos(self.infos)
		if rep is 'error':
			self.end()

	def indexation(self):
		for infoswebpage in self.infos:
			id0 = self.data_base.get_id(infoswebpage['url'])
			if id0 is 'error':
				self.end()
			speak('indexation : {0} {1}'.format(
				str(id0[0]), infoswebpage['url']))
			rep = self.inverted_index.append_doc(infoswebpage, id0[0])
			if rep is 'del':
				self.data_base.del_one_doc(infoswebpage['url'], 'index_url')

	def send_index(self):
		rep = self.ftp.send_index(self.inverted_index.getIndex())
		if rep is 'error':
			self.end()

	def suggestions(self):
		"""se connecter à la base et récupéré 5 url à crawler
		supprimer les urls de la table suggestions
		crawler les urls
		envoyé les docs
		indexé les doc
		reprendre la boucle
		"""
		speak('suggestions : ')
		suggestions = self.data_base.suggestions()
		if suggestions is 'error':
			speak('erreur de récupération des suggestions')
			self.end() # qu-est-ce qu'on fait ?
		else:
			suggestions = self.web_site_infos.clean_links(suggestions)
			for url in suggestions:
				self.crawl_web_site(url)
			self.send_DB()
			self.indexation()
			self.infos.clear() # reset the list of dict of informations of webs sites

	def end(self):
		self.send_index()
		speak('le programme vas se fermer')
		leaving()

if __name__ == '__main__':
	crawler = Crawler6()
	crawler.start()
	print('fin/end')
	system('pause')

"""
à faire : 
- prendre l'url de l'icone du site
- suggestions : netocentre passe pas bien
- erreur de nettoyage des liens quand ya des " : http://www.telerama.fr/breve/"Films de Cannes 2014"

à revoir : 
- archivage
- revoir le nom de toutes les variables

à tester:
- ne pas augmenter mettre à jour quand on a visité le site peu de temps avant (on tourne peut-être en rond mais faudrait peut-être quand même incrémenter la papularité, sans mettre à jour le reste ?)
- configparser : l'arrêt
- le fichiers liens se remplicent rapidement

plus tard :
- prendre la liste des les liens de départ sur le site Swiftea
- passer l'index inversé dans la base de donnée
- requettes par minute

remarque : 
- erreur handle_entityref
- n°31 et 7:50 dans les mots-clefs ?
- l'id dans la DB correspond à la ligne dans les fichiers statistiques : c'esr dar !
- l'indexation est vraiment trop longue !
- pourquoi un id dans la table suggestions ?
- score : 1.5 (encodage, css, langue)
- refaire les erreur dans database_swiftea
- prendre le title des image pour mots-clés
- utilisé un module pour faire les documentations des modules

suggestions : 
- l'utilisateur peut signaler une erreur d'information ou 404

libraries :
mypysql
reppy
"""

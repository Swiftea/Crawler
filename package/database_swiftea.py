#!/usr/bin/python3

"""Functions of managemet of database."""

import socket # for timeout error
from datetime import datetime, timedelta


from package.module import speak
from package.database_pymysql import DataBase

__author__ = "Seva Nathan"

class DataBase_swiftea(DataBase):
	def __init__(self, host, user, password, base):
		"""Build the class."""
		DataBase.__init__(self, host, user, password, base)

	def send_infos(self, infos):
		"""Add informations in the database and return 'go' or 'stop'."""
		for key, value  in enumerate(infos): # boucle compliqué pour rien : seul key et infos est utilisé ?
			result, rep = self.send_command("SELECT popularity, last_crawl FROM index_url WHERE url = %s", (infos[key]['url'],))
			if 'error' in rep:
				speak('la demande de popularity et last_crawl a échoué : ' + rep, 16)
				return 'error'
			if result != ():
				# url funded in the data base, there is a answer :
				last_crawl = result[0][1] # datetime.datetime object
				if (datetime.now() - last_crawl) > timedelta(minutes=10): # 30 jours ?
					# cela fait plus {} minutes que l'on a pas crawlé ce site web
					pop = result[0][0]+1
					speak('mise à jour de site : ' + infos[key]['url'])
					result, rep = self.send_command(
"""UPDATE index_url
SET title=%s, description=%s, last_crawl=NOW(), lang=%s, popularity=%s, nb_words=%s, score=%s, nb_words=%s
WHERE url = %s """, \
(infos[key]['title'], infos[key]['description'], infos[key]['language'], pop, infos[key]['nb_words'], infos[key]['score'], infos[key]['nb_words'], infos[key]['url']))
					if 'error' in rep:
						speak('la mise à jour a échoué : ' + rep, 16)
						return 'error'
				else:
					# cela fait moins de {} minutes que l'on a crawlé ce site web
					speak('pas de mise a jour, site récemment cralwé')
			else:
				# url not funded in data base, the url don't exist in the database, we add it :
				speak('ajout : ' + infos[key]['url'])
				result, rep = self.send_command(
"""INSERT INTO index_url (title, description, url, first_crawl, last_crawl, lang, likes, popularity, score, nb_words)
VALUES (%s, %s, %s, NOW(), NOW(), %s, 0, 1, %s, %s)""", \
(infos[key]['title'], infos[key]['description'], infos[key]['url'],	infos[key]['language'], infos[key]['score'], infos[key]['nb_words']))
				if 'error' in rep:
					speak("l'ajout a échoué : " + rep, 16)
					return 'error'
		# end loop
		return 'ok'

	def get_user(self):
		"""Get back user name."""
		result, rep = self.send_command("SELECT pseudo FROM users")
		if 'error' in rep:
			speak('la demande du pseudo a échoué : ' + rep, 16)
		return result

	def drop_BDD(self):
		"""WARNING !!! Delete all documents in database."""
		oui = input('Voulez-vous vraiment vider la table ? : ')
		if oui == 'oui':
			result, rep = self.send_command("TRUNCATE TABLE index_url")
			if 'error' in rep:
				speak('le vidage de la table a échoué : ', rep, 16)
			else:
				speak('table purgée !')
		else:
			speak("la table n'as pas été vidée.")

	def get_id(self, url):
		"""Return the id of a document in database."""
		result, rep = self.send_command("SELECT id FROM index_url WHERE url = %s",	(url,))
		if 'error' in rep:
			speak("erreur de récupération de l'id0 : " + rep, 18)
			return 'error'
		else:
			return result[0]

	def del_one_doc(self, url, table):
		"""Delete one document of database knowing url."""
		speak('suppression du document : ' + url)
		result, rep = self.send_command("DELETE FROM {} WHERE url = %s".format(table), (url,))
		if 'error' in rep:
			speak("le documment n'a pas été supprimé : {0}, {1}".format(url, rep), 17)

	def suggestions(self):
		"""Return the list of url in Suggestions."""
		result, rep = self.send_command("SELECT url FROM suggestions LIMIT 5")
		if 'error' in rep:
			speak("la demande de l'url a échoué : " + rep, 16)
			return 'error'
		else:
			suggest_links = list()
			for elements in result:
				if len(suggest_links) < 5:
					suggest_links.append(elements[0])
					self.del_one_doc(elements[0], 'suggestions')
			return suggest_links
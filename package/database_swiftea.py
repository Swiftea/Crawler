#!/usr/bin/python3

"""Functions of managemet of database."""

import socket # for timeout error
from datetime import datetime, timedelta


from package.module import speak
from package.database_pymysql import DataBase
from package.data import CRAWL_DELAY

__author__ = "Seva Nathan"

class DataBase_swiftea(DataBase):
	def __init__(self, host, user, password, base):
		"""Build the class."""
		DataBase.__init__(self, host, user, password, base)

	def send_infos(self, infos):
		"""Add informations in the database and return 'ok' or 'error'."""
		for key, value  in enumerate(infos):
			result, rep = self.send_command("SELECT popularity, last_crawl FROM index_url WHERE url = %s", (infos[key]['url'],))
			if 'error' in rep:
				# the query for popularity and last_crawl has failed
				speak('la demande de popularity et last_crawl a échoué : ' + rep, 16)
				return 'error'
			if result != ():
				# url funded in the data base, there is a answer :
				last_crawl = result[0][1] # datetime.datetime object
				if (datetime.now() - last_crawl) > timedelta(minutes=CRAWL_DELAY): # must be days, but minutes is better for tests
					# the program already crawl this web site 30 days ago
					popularity = result[0][0]+1
					speak('mise à jour de ' + infos[key]['url']) # update the document : url
					result, rep = self.send_command(
"""UPDATE index_url
SET title=%s, description=%s, last_crawl=NOW(), lang=%s, popularity=%s, nb_words=%s, score=%s, nb_words=%s, favicon=%s
WHERE url = %s """, \
(infos[key]['title'], infos[key]['description'], infos[key]['language'], popularity, infos[key]['nb_words'], infos[key]['score'], infos[key]['nb_words'], infos[key]['favicon'], infos[key]['url']))
					if 'error' in rep:
						speak('la mise à jour a échoué : ' + rep, 16) # update failed
						return 'error'
				else:
					# already crawl 30 days ago
					speak('No updates, already crawled recently') # no update, web site recently crawl
			else:
				# url not finded in database, the url don't exist in the database, we add it :
				speak('ajout : ' + infos[key]['url']) # adding : url
				result, rep = self.send_command(
"""INSERT INTO index_url (title, description, url, first_crawl, last_crawl, lang, likes, popularity, score, nb_words, favicon)
VALUES (%s, %s, %s, NOW(), NOW(), %s, 0, 1, %s, %s, %s)""", \
(infos[key]['title'], infos[key]['description'], infos[key]['url'],	infos[key]['language'], infos[key]['score'], infos[key]['nb_words'], infos[key]['favicon']))
				if 'error' in rep:
					speak("Failed to add : " + rep, 16) # the adding failed
					return 'error'
		# end loop
		return 'ok' # all operations are correct

	def get_user(self): # not use
		"""Get back user name."""
		result, rep = self.send_command("SELECT pseudo FROM users")
		if 'error' in rep:
			speak('Failed to get username : ' + rep, 16)
		return result

	def drop_BDD(self): # not use
		"""WARNING !!! Delete all documents in database."""
		# do you realy want to drop the table ?
		response = input('Do you really want to delete all entries in index ? : ')
		if response == 'yes':
			result, rep = self.send_command("TRUNCATE TABLE index_url")
			if 'error' in rep:
				# drop table failed
				speak('Failed to empty table : ', rep, 16)
			else:
				# table droped
				speak('Table is empty !')
		else:
			# the table didn't be drop
			speak("Not empty !")

	def get_id(self, url):
		"""Return the id of a document in database."""
		result, rep = self.send_command("SELECT id FROM index_url WHERE url = %s", (url,))
		if 'error' in rep:
			speak("Failed to get id : " + rep, 18)
			return 'error'
		else:
			return result[0]

	def del_one_doc(self, url, table):
		"""Delete the document corresponding to url from table."""
		speak('suppression du document : ' + url) # delete the document
		result, rep = self.send_command("DELETE FROM {} WHERE url = %s".format(table), (url,))
		if 'error' in rep:
			# document is not remove
			speak("Doc is not remove : {0}, {1}".format(url, rep), 17)

	def suggestions(self):
		"""Return the list of url in Suggestions and delete their."""
		result, rep = self.send_command("SELECT url FROM suggestions LIMIT 5")
		if 'error' in rep:
			speak("Failed to get url : " + rep, 16) # query failed
			return 'error'
		else:
			suggest_links = list()
			for elements in result:
				if len(suggest_links) < 5:
					suggest_links.append(elements[0])
					self.del_one_doc(elements[0], 'suggestions')
			return suggest_links

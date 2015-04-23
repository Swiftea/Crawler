#!/usr/bin/python3

from datetime import datetime


from package.module import speak
from package.database_manager import DatabaseManager
from package.data import CRAWL_DELAY

__author__ = "Seva Nathan"

class DatabaseSwiftea(DatabaseManager):
	"""Class to manage Swiftea database

	:param host: hostname of the ftp server
	:type host: str
	:param user: username to use for connexion
	:type user: str
	:param password: password to use for connexion
	:type password: str
	:param name: name of database
	:type name: str

	"""

	def __init__(self, host, user, password, name):
		"""Build manager"""
		DatabaseManager.__init__(self, host, user, password, name)

	def send_infos(self, infos):
		"""send informations in database

		:param infos: informations to send to database
		:type infos: list
		:return: true if an error occured

		"""
		for key, value in enumerate(infos):
			result, response = self.send_command("SELECT popularity, last_crawl FROM index_url WHERE url = %s", (infos[key]['url'],), True)
			if response != 'Send command : ok':
				speak('Popularity and last_crawl query failed : ' + response, 16)
				return True
			if result != ():
				# url found in database, there is a answer :
				last_crawl = result[0][1] # datetime.datetime object
				if (datetime.now() - last_crawl) > CRAWL_DELAY:
					# the program already crawled this website
					response = self.update(infos[key], result[0][0]+1)
					if response:
						return True
				else:
					# already crawled
					speak('No updates, already crawled recently')
			else:
				# url not found in database, the url don't exists in the database, we add it :
				response = self.insert(infos[key])
				if response:
					return True
		# end loop
		return False # all is correct

	def update(self, infos, popularity):
		"""Update a doc in database

		:param infos: doc infos
		:type infos: dict()
		:param popularity: new doc popularity
		:type popularity: int
		:return: true is an arror occured

		"""
		speak('Updating : ' + infos['url'])
		result, response = self.send_command(
"""UPDATE index_url
SET title=%s, description=%s, last_crawl=NOW(), lang=%s, popularity=%s, score=%s, favicon=%s
WHERE url = %s """, (infos['title'], infos['description'], infos['language'], popularity, infos['score'], infos['favicon'], infos['url']))
		if response != 'Send command : ok':
			speak('Failed to update : ' + response, 16)
			return True
		else:
			return False

	def insert(self, infos):
		"""Update a doc in database

		:param infos: doc infos
		:type infos: dict()
		:return: true is an arror occured

		"""
		speak('Adding : ' + infos[key]['url'])
		result, response = self.send_command(
"""INSERT INTO index_url (title, description, url, first_crawl, last_crawl, lang, likes, popularity, score, favicon)
VALUES (%s, %s, %s, NOW(), NOW(), %s, 0, 1, %s, %s)""", \
(infos['title'], infos['description'], infos['url'], infos['language'], infos['score'], infos['favicon']))
		if response != 'Send command : ok':
			speak("Failed to add : " + response, 16)
			return True
		else:
			return False

	def get_doc_id(self, url):
		"""Get id of a webpage in database

		:param url: url of webpage
		:type url: str
		:return: id of webpage

		"""
		result, response = self.send_command("SELECT id FROM index_url WHERE url = %s", (url,))
		if response != 'Send command : ok':
			speak("Failed to get id : " + response, 18)
			return None
		else:
			return str(result[0])

	def del_one_doc(self, url, table):
		"""Delete document corresponding to url from table

		:param url: url of webpage
		:type url: str
		:param table: table where given url is
		:type table: str

		"""
		speak('suppression du document : ' + url)
		result, response = self.send_command("DELETE FROM {} WHERE url = %s".format(table), (url,))
		if response != 'Send command : ok':
			speak("Doc not removed : {0}, {1}".format(url, response), 17)

	def suggestions(self):
		""":return: list of url in Suggestions table and delete them"""
		result, response = self.send_command("SELECT url FROM suggestions LIMIT 5", fetchall=True)
		if response != 'Send command : ok':
			speak("Failed to get url : " + response, 16)
			return None
		else:
			suggested_links = list()
			for element in result:
				if len(suggested_links) < 5:
					suggested_links.append(element[0])
					self.del_one_doc(element[0], 'suggestions')
			return suggested_links

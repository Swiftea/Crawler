#!/usr/bin/python3

from datetime import datetime

from package.module import speak
from package.database_manager import DatabaseManager
from package.data import CRAWL_DELAY

class DatabaseSwiftea(DatabaseManager):
	"""Class to manage Swiftea database.

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
		DatabaseManager.__init__(self, host, user, password, name)


	def send_infos(self, infos):
		"""send documents informations to database.

		:param infos: informations to send to database
		:type infos: list
		:return: true if an error occured
		"""
		for webpage_infos in infos:
			result, response = self.send_command("SELECT popularity, last_crawl FROM index_url WHERE url = %s", (webpage_infos['url'],), True)
			if response != 'Send command : ok':
				speak('Popularity and last_crawl query failed : ' + response, 16)
				return True
			if result != ():
				# Url found in database, there is a answer :
				last_crawl = result[0][1]  # datetime.datetime object
				if (datetime.now() - last_crawl) > CRAWL_DELAY:
					# The program already crawled this website
					response = self.update(webpage_infos, result[0][0]+1)
					if response:
						return True
				else:
					speak('No updates, recently crawled')
			else:
				# Url not found in database, the url don't exists in the database, we add it:
				response = self.insert(webpage_infos)
				if response:
					return True
		# End of loop
		return False  # All is correct


	def update(self, infos, popularity):
		"""Update a document in database.

		:param infos: doc infos
		:type infos: dict()
		:param popularity: new doc popularity
		:type popularity: int
		:return: true is an arror occured
		"""
		speak('Updating : ' + infos['url'])
		response = self.send_command(
"""UPDATE index_url
SET title=%s, description=%s, last_crawl=NOW(), lang=%s, popularity=%s, score=%s, favicon=%s
WHERE url = %s """, (infos['title'], infos['description'], infos['language'], popularity, infos['score'], infos['favicon'], infos['url']))
		if response[1] != 'Send command : ok':
			speak('Failed to update : ' + response[1], 16)
			return True
		else:
			return False


	def insert(self, infos):
		"""Insert a new document in database.

		:param infos: doc infos
		:type infos: dict()
		:return: true is an arror occured
		"""
		speak('Adding : ' + infos['url'])
		response = self.send_command(
"""INSERT INTO index_url (title, description, url, first_crawl, last_crawl, lang, likes, popularity, score, favicon)
VALUES (%s, %s, %s, NOW(), NOW(), %s, 0, 1, %s, %s)""", \
(infos['title'], infos['description'], infos['url'], infos['language'], infos['score'], infos['favicon']))
		if response[1] != 'Send command : ok':
			speak("Failed to add : " + response[1], 16)
			return True
		else:
			return False


	def get_doc_id(self, url):
		"""Get id of a document in database.

		:param url: url of webpage
		:type url: str
		:return: id of webpage or None if not found
		"""
		result, response = self.send_command("SELECT id FROM index_url WHERE url = %s", (url,))
		if response != 'Send command : ok':
			speak("Failed to get id : " + response, 18)
			return None
		else:
			return str(result[0])


	def del_one_doc(self, url, table):
		"""Delete document corresponding to url from the given table.

		:param url: url of webpage
		:type url: str
		:param table: table where given url is
		:type table: str
		:return: status message
		"""
		speak('suppression du document : ' + url)
		response = self.send_command("DELETE FROM {} WHERE url = %s".format(table), (url,))
		if response[1] != 'Send command : ok':
			speak("Doc not removed : {0}, {1}".format(url, response[1]), 17)
		return response[1]


	def suggestions(self):
		"""Get the five first url from Suggestions table and delete them.

		:return: list of url in Suggestions table and delete them
		"""
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

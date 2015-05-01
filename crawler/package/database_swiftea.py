#!/usr/bin/python3

from datetime import datetime

from package.module import tell, convert_secure, url_is_secure
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


	def send_doc(self, webpage_infos):
		"""send documents informations to database.

		:param infos: informations to send to database
		:type infos: list
		:return: True if an error occured

		"""
		result, response = self.send_command("SELECT popularity, last_crawl FROM index_url WHERE url = %s", (webpage_infos['url'],), True)
		if 'error' in response:
			tell('Popularity and last_crawl query failed: ' + response, 16)
			return True
		if result != ():
			# Url found in database, there is a answer:
			last_crawl = result[0][1]  # datetime.datetime object
			if (datetime.now() - last_crawl) > CRAWL_DELAY:
				# The program already crawled this website
				error = self.update(webpage_infos, result[0][0]+1)
				if error:
					return True
			else:
				tell('No updates, recently crawled', severity=0)
		else:
			# Url not found in database, the url don't exists in the database, we add it:
			error = self.insert(webpage_infos)
			if error:
				return True
		return False  # All is correct


	def update(self, infos, popularity):
		"""Update a document in database.

		:param infos: doc infos
		:type infos: dict()
		:param popularity: new doc popularity
		:type popularity: int
		:return: True is an arror occured

		"""
		tell('Updating ' + infos['url'])
		response = self.send_command(
"""UPDATE index_url
SET title=%s, description=%s, last_crawl=NOW(), lang=%s, popularity=%s, score=%s, homepage=%s, favicon=%s
WHERE url = %s """, (infos['title'], infos['description'], infos['language'], popularity, infos['score'],\
	infos['homepage'], infos['favicon'], infos['url']))
		if 'error' in  response[1]:
			tell('Failed to update: ' + response[1], 9)
			return True
		else:
			return False


	def insert(self, infos):
		"""Insert a new document in database.

		:param infos: doc infos
		:type infos: dict()
		:return: True is an arror occured

		"""
		tell('Adding ' + infos['url'])
		response = self.send_command(
"""INSERT INTO index_url (title, description, url, first_crawl, last_crawl, lang, likes, popularity, score, homepage, favicon)
VALUES (%s, %s, %s, NOW(), NOW(), %s, 0, 1, %s, %s, %s)""", \
(infos['title'], infos['description'], infos['url'], infos['language'], infos['score'], infos['homepage'], infos['favicon']))
		if 'error' in  response[1]:
			tell('Failed to add: ' + response[1], 10)
			return True
		else:
			return False


	def get_doc_id(self, url, table='index_url'):
		"""Get id of a document in database.

		:param url: url of webpage
		:type url: str
		:param table: table, default to index_url
		:type table: str
		:return: id of webpage or None if not found

		"""
		result, response = self.send_command("SELECT id FROM {} WHERE url = %s".format(table), (url,))
		if 'error' in  response[1]:
			tell('Failed to get id: ' + response, 11)
			return None
		else:
			return str(result[0])


	def del_one_doc(self, url, table='index_url'):
		"""Delete document corresponding to url from the given table.

		:param url: url of webpage
		:type url: str
		:param table: table where given url is
		:type table: str
		:param table: table, default to index_url
		:type table: str
		:return: status message

		"""
		tell('Delete from {} doc: '.format(table) + url)
		response = self.send_command("DELETE FROM {} WHERE url = %s".format(table), (url,))
		if 'error' in  response[1]:
			tell('Doc not removed: {0}, {1}'.format(url, response[1]), 12)
		return response[1]


	def suggestions(self):
		"""Get the five first url from Suggestions table and delete them.

		:return: list of url in Suggestions table and delete them

		"""
		result, response = self.send_command("SELECT url FROM suggestions LIMIT 5", fetchall=True)
		if 'error' in  response[1]:
			tell('Failed to get url: ' + response, 13)
			return None
		else:
			suggested_links = list()
			for element in result:
				if len(suggested_links) < 5:
					suggested_links.append(element[0])
					self.del_one_doc(element[0], 'suggestions')
			return suggested_links


	def doc_exists(self, url, table='index_url'):
		"""Check if url is in database.

		:param url: url corresponding to doc
		:type url: str
		:param table: table, default to index_url
		:type table: str
		:return: True if doc exists

		"""
		result, response = self.send_command("SELECT EXISTS(SELECT * FROM {} WHERE url=%s)".format(table), (url,))
		if 'error' in  response:
			tell('Failed to check row: ' + response, 14)
			return None
		if result[0] == 1:
			return True
		else:
			return False

	def https_duplicate(self, old_url):
		"""Avoid https and http duplicate.

		If old url is secure (https), must delete insecure url if exists,
		then return secure url (old url).
		If old url is insecure (http), must delete it if secure url exists,
		then return secure url (new url)

		:param old_url: old url
		:type old_url: str
		:return: url to add and url to delete

		"""
		tell('url to send: ' + old_url, severity=-1)
		new_url = convert_secure(old_url)
		new_exists = self.doc_exists(new_url)

		if url_is_secure(old_url):
			# old_url start with https
			if new_exists:  # Start with http
				tell('insecure exists', severity=-1)
				return old_url, new_url
			else:
				tell('return secure, old', severity=-1)
				return old_url, None
		else:
			# old_url is insecure, start with http
			if new_exists:  # Secure url exists
				if self.doc_exists(old_url):  # Insecure exists
					return new_url, old_url
				else:
					tell('return secure, new', severity=-1)
					return new_url, None
			else:
				tell('return insecure, old', severity=-1)
				return old_url, None

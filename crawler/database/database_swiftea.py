#!/usr/bin/env python3

"""Define a class that deal with the high level database manager."""

from datetime import datetime

from swiftea_bot.module import tell
from swiftea_bot.data import CRAWL_DELAY
from database.database_manager import DatabaseManager
import database.database as database


class DatabaseSwiftea(DatabaseManager):
	"""Class to manage Swiftea database.

	:param host: hostname of the db server
	:type host: str
	:param user: username to use for connection
	:type user: str
	:param password: password to use for connection
	:type password: str
	:param name: name of database
	:type name: str

	"""
	def __init__(self, host, user, password, name, table, domaine):
		DatabaseManager.__init__(self, host, user, password, name)
		self.t = table

	def send_doc(self, webpage_infos):
		"""Send document informations to database.

		:param infos: informations to send to database
		:type infos: list
		:return: True if an error occured

		"""
		error = False  # no error
		response = self.connection()
		result, response = self.send_command(
			"SELECT popularity, last_crawl FROM {} WHERE url = %s".format(self.t),
			(webpage_infos['url']), True)
		if 'error' in response:
			tell('Popularity and last_crawl query failed: ' + response, 16)
			error = True
		if result != ():
			# Url found in database, there is an answer:
			last_crawl = result[0][1]  # datetime.datetime object
			if (datetime.now() - last_crawl) > CRAWL_DELAY:
				# The program have already crawled this website
				response = self.update(webpage_infos, result[0][0]+1)
				if error:
					error = True
			else:
				tell('Recently crawled: ' + webpage_infos['url'])
		else:
			# Url not found in database, the url doesn't exist in the database,
			# we add it:
			error = self.insert(webpage_infos)
			if error:
				error = True
		self.close_connection()
		return error  # All is correct

	def update(self, infos, popularity):
		"""Update a document in database.

		:param infos: doc infos
		:type infos: dict()
		:param popularity: new doc popularity
		:type popularity: int
		:return: True is an arror occured

		"""
		tell('Updating ' + infos['url'])
		cmd = """
UPDATE {} SET title=%s, description=%s, last_crawl=NOW(), language=%s,
popularity=%s, score=%s, homepage=%s, sanesearch=%s, favicon=%s
WHERE url = %s""".format(self.t)
		response = self.send_command(cmd, (infos['title'], infos['description'],
			infos['language'], popularity, infos['score'], infos['homepage'],
			infos['sanesearch'], infos['favicon'], infos['url'])
		 )
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
"""INSERT INTO {} (title, description, url, first_crawl, last_crawl, language,
popularity, score, homepage, sanesearch, favicon)
VALUES (%s, %s, %s, NOW(), NOW(), %s, 1, %s, %s, %s, %s)""".format(self.t),
			(infos['title'], infos['description'], infos['url'],
			infos['language'], infos['score'], infos['homepage'],
			infos['sanesearch'], infos['favicon'])
		)
		if 'error' in response[1][1]:
			tell('Failed to add: ' + str(response), 10)
			return True
		else:
			return False

	def get_doc_id(self, url):
		"""Get id of a document in database.

		:param url: url of webpage
		:type url: str
		:return: id of webpage or None if not found

		"""
		result, response = self.send_command("SELECT id FROM {} WHERE url = %s".format(self.t), (url))
		if 'error' in  response[1]:
			tell('Failed to get id: ' + response, 11)
			return None
		else:
			return str(result[0])

	def del_one_doc(self, url, table=None):
		"""Delete document corresponding to url.

		:param url: url of webpage
		:type url: str
		:return: status message

		"""
		if table is None:
			table = self.t
		tell('Delete from {} doc: {}'.format(table,  url))
		response = self.send_command("DELETE FROM {} WHERE url = %s".format(table), (url))
		if 'error' in  response[1] or response[1][1] != 'Send command: ok':
			tell('Doc not removed: {0}, {1}'.format(url, response[1]), 12)
		return response[1]

	def suggestions(self):
		"""Get the five first URLs from Suggestion table and delete them.

		:return: list of url in Suggestion table and delete them

		"""
		result, response = self.send_command("SELECT url FROM suggestion LIMIT 5", fetchall=True)
		if 'error' in  response[1] or result is None:
			tell('Failed to get url: ' + response, 13)
			return None
		else:
			suggested_links = list()
			for element in result:
				if len(suggested_links) < 5:
					suggested_links.append(element[0])
					self.del_one_doc(element[0], 'suggestion')
			return suggested_links

	def doc_exists(self, url):
		"""Check if `url` is in database.

		:param url: url corresponding to doc
		:type url: str
		:return: True if doc exists

		"""
		result, response = self.send_command("SELECT EXISTS(SELECT * FROM {} WHERE url=%s)".format(self.t), (url))
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
		new_url = database.convert_secure(old_url)
		new_exists = self.doc_exists(new_url)

		if database.url_is_secure(old_url):
			# old_url start with https
			if new_exists:  # Start with http
				return old_url, new_url
			else:
				return old_url, None
		else:
			# old_url is insecure, start with http
			if new_exists:  # Secure url exists
				if self.doc_exists(old_url):  # Insecure exists
					return new_url, old_url
				else:
					return new_url, None
			else:
				return old_url, None

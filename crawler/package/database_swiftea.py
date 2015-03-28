#!/usr/bin/python3

"""Functions of managemet of database."""

import socket # for timeout error
from datetime import datetime


from package.module import speak
from package.database_manager import DatabaseManager
from package.data import CRAWL_DELAY, CRAWL_IMG_DELAY

__author__ = "Seva Nathan"

class DatabaseSwiftea(DatabaseManager):
	def __init__(self, host, user, password, name):
		"""Build the class."""
		DatabaseManager.__init__(self, host, user, password, name)

	def send_infos(self, infos):
		"""Add informations in db and return True if an error occured."""
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
					popularity = result[0][0]+1
					speak('Updating : ' + infos[key]['url'])
					result, response = self.send_command(
"""UPDATE index_url
SET title=%s, description=%s, last_crawl=NOW(), lang=%s, popularity=%s, nb_words=%s, score=%s, nb_words=%s, favicon=%s
WHERE url = %s """, \
(infos[key]['title'], infos[key]['description'], infos[key]['language'], popularity, infos[key]['nb_words'], infos[key]['score'], infos[key]['nb_words'], infos[key]['favicon'], infos[key]['url']))
					if response != 'Send command : ok':
						speak('Failed to update : ' + response, 16) # update failed
						return True
				else:
					# already crawled
					speak('No updates, already crawled recently')
			else:
				# url not found in database, the url don't exists in the database, we add it :
				speak('Adding : ' + infos[key]['url'])
				result, response = self.send_command(
"""INSERT INTO index_url (title, description, url, first_crawl, last_crawl, lang, likes, popularity, score, nb_words, favicon)
VALUES (%s, %s, %s, NOW(), NOW(), %s, 0, 1, %s, %s, %s)""", \
(infos[key]['title'], infos[key]['description'], infos[key]['url'],	infos[key]['language'], infos[key]['score'], infos[key]['nb_words'], infos[key]['favicon']))
				if response != 'Send command : ok':
					speak("Failed to add : " + response, 16)
					return True
		# end loop
		return False # all is correct

	def send_images(self, images):
		"""Base name : index_img ; id, url, alt, last_crawl

		images is a list of tuple (ulr, alt)
		Return True if an error occured.

		"""
		for key, image in enumerate(images):
			# images is a tuple (url, alt)
			result, response = self.send_command("SELECT last_crawl FROM index_img WHERE url = %s", (image[0],))
			if response != 'Send command : ok':
				speak('Failed to get last_crawl when send image : ' + response, 27)
				return True
			if result is not None:
				# crawl delay :
				if (datetime.now() - result[0]) > CRAWL_IMG_DELAY:
					speak('Updating image : ' + image[1])
					result, response = self.send_command("UPDATE index_img SET alt=%s, last_crawl=NOW() WHERE url=%s", (image[1], image[0]))
					if response != 'Send command : ok':
						speak('Failed to update : ' + response, 25)
						return True
				else:
					speak('No update image, already crawled recently')
			else:
				speak('Adding image : ' + image[1])
				result, response = self.send_command("INSERT INTO index_img (url, alt, last_crawl) VALUES (%s, %s, NOW())", (image[0], image[1]))
				if response != 'Send command : ok':
					speak('Failed to add image : ' + response, 26)
		return False # all is correct

	def get_doc_id(self, url):
		"""Return the id of a document in database."""
		result, response = self.send_command("SELECT id FROM index_url WHERE url = %s", (url,))
		if response != 'Send command : ok':
			speak("Failed to get id : " + response, 18)
			return None
		else:
			return str(result[0])

	def del_one_doc(self, url, table):
		"""Delete the document corresponding to url from table."""
		speak('suppression du document : ' + url)
		result, response = self.send_command("DELETE FROM {} WHERE url = %s".format(table), (url,))
		if response != 'Send command : ok':
			speak("Doc not removed : {0}, {1}".format(url, response), 17)

	def suggestions(self):
		"""Return the list of url in Suggestions and delete them."""
		result, response = self.send_command("SELECT url FROM suggestions LIMIT 5", all=True)
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

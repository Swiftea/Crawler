#!/usr/bin/python3

"""Manage the connection to web sites."""

__author__ = "Seva Nathan"

import requests # to get back the source code


from reppy.cache import RobotsCache
from reppy.exceptions import ServerError


from package.data import USER_AGENT, HEADERS
from package.module import speak
from package.searches import Parser_encoding

class WebConnexion:
	"""Manage the web connexion with the page to crawl."""
	def __init__(self):
		self.reqrobots = RobotsCache()
		self.parser = Parser_encoding()

	def get_code(self, url):
		"""Return code, nofollow and score."""
		if url.endswith('!nofollow!'):
			url = url[:-10]
			nofollow = True
		else:
			nofollow = False
		try:
			r = requests.get(url, headers=HEADERS)
		except requests.exceptions.ConnectionError:
			speak('erreur de connexion au site web (ConnectionError)', 6)
			return 'continue', nofollow, 0
		except requests.exceptions.Timeout: # peut mieux faire ?
			speak('le site web ne répond pas', 7)
			return 'continue', nofollow, 0
		except requests.exceptions.RequestException as error:
			speak('erreur de connexion au site web : ' + str(error), 8)
			return 'continue', nofollow, 0
		else:
			try:
				allowed = self.reqrobots.allowed(url, USER_AGENT)
			except ServerError as error:
				speak('error robot.txt : ' + str(error), 24)
				allowed = True
			if r.status_code == requests.codes.ok and \
				r.headers['Content-Type'].startswith('text/html') and \
				allowed:
				# searche encoding of web page :
				r.encoding, score = self.searche_encoding(r)
				return r.text, nofollow, score
			else:
				return 'continue', nofollow, 0

	def searche_encoding(self, r):
		"""Return encoding of r's requests web page and the score."""
		# searche in headers : 
		headers = str(r.headers).lower()
		charset = headers.find('charset')
		end_charset = headers.find('\'', charset)
		if charset != -1 and end_charset != -1:
			return headers[charset+8:end_charset], .5
		else:
			# searche in source code:
			self.parser.feed(r.text)
			if self.parser.encoding is not None:
				return self.parser.encoding, .5
			else:
				# encoding not given
				speak("pas d'indication d'encodage", 9)
				return 'utf-8', 0

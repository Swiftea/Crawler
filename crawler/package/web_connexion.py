#!/usr/bin/python3

"""Manage the connection to web sites."""

__author__ = "Seva Nathan"

import requests # to get back the source code


from reppy.cache import RobotsCache
from reppy.exceptions import ServerError


from package.data import USER_AGENT, HEADERS, TIMEOUT
from package.module import speak, get_base_url
from package.parsers import Parser_encoding

class WebConnexion:
	"""Manage the web connexion with the page to crawl."""
	def __init__(self):
		self.reqrobots = RobotsCache()
		self.parser_encoding = Parser_encoding()

	def get_code(self, url):
		"""Return code, is_nofollow and score."""
		if url.endswith('!nofollow!'):
			url = url[:-10]
			is_nofollow = True
		else:
			is_nofollow = False
		try:
			request = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
		except requests.exceptions.Timeout:
			speak('Website not responding : ' + url, 7)
			return None, is_nofollow, 0
		except requests.exceptions.RequestException as error:
			speak('Failed to connect to website : {}, {}'.format(str(error), url), 8)
			return None, is_nofollow, 0
		else:
			try:
				requests.get(get_base_url(url) + '/robots.txt', timeout=TIMEOUT)
			except requests.exceptions.RequestException as error:
				speak('Error robot.txt (2) : ' + str(error), 24)
				allowed = True
			else:
				try:
					allowed = self.reqrobots.allowed(url, USER_AGENT)
				except ServerError as error:
					speak('Error robot.txt : ' + str(error), 24)
					allowed = True
			finally:
				if request.status_code == requests.codes.ok and request.headers.get('Content-Type', '').startswith('text/html') and	allowed:
					# search encoding of webpage :
					request.encoding, score = self.search_encoding(request)
					return request.text, is_nofollow, score
				else:
					speak('Info webpage : status code=' + str(request.status_code) + ', Content-Type=' + request.headers.get('Content-Type', '') + ', robots permission=' + str(allowed) + ', nofollow=' + str(is_nofollow))
					return None, is_nofollow, 0

	def search_encoding(self, request):
		"""Return encoding of webpage request and the score."""
		# search in headers :
		headers = str(request.headers).lower()
		charset = headers.find('charset')
		end_charset = headers.find('\'', charset)
		if charset != -1 and end_charset != -1:
			return headers[charset+8:end_charset], .5
		else:
			# search in source code:
			self.parser_encoding.feed(request.text)
			if self.parser_encoding.encoding is not None:
				return self.parser_encoding.encoding, .5
			else:
				speak("No encoding", 9)
				return 'utf-8', 0

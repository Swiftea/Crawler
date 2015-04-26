#!/usr/bin/python3

"""Connexion to webpage are manage with requests module.
Thoses errors are waiting for: timeout with socket module and with urllib3 mudule
and all RequestException errors."""

__author__ = "Seva Nathan"

import requests


from reppy.cache import RobotsCache
from reppy.exceptions import ServerError


from package.data import USER_AGENT, HEADERS, TIMEOUT
from package.module import speak, no_connexion
from package.parsers import Parser_encoding

class WebConnexion(object):
	"""Manage the web connexion with the page to crawl"""
	def __init__(self):
		"""Build manager"""
		self.reqrobots = RobotsCache()
		self.parser_encoding = Parser_encoding()

	def get_code(self, url):
		"""Get source code of given url

		:param url: url of webpage
		:type url: str
		:return: source code, True if no take links and score

		"""
		is_nofollow, url = self.is_nofollow(url)
		try:
			request = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
		except resuests.packages.urllib3.exceptions.ReadTimeoutError:
			speak('Website not responding (urllib3): ' + url, 7)
			return None, False, 0
		except requests.exceptions.Timeout:
			speak('Website not responding: ' + url, 7)
			return None, False, 0
		except requests.exceptions.RequestException as error:
			speak('Failed to connect to website: {}, {}'.format(str(error), url), 8)
			if no_connexion():
				return 'no_connexion', is_nofollow, 0
			else:
				return None, False, 0
		else:
			allowed = self.check_robots_perm(url)
			if request.status_code == requests.codes.ok and request.headers.get('Content-Type', '').startswith('text/html') and	allowed:
				# search encoding of webpage :
				request.encoding, score = self.search_encoding(request.headers, request.text)
				return request.text, is_nofollow, score
			else:
				speak('Webpage infos: status code=' + str(request.status_code) + ', Content-Type=' + \
					request.headers.get('Content-Type', '') + ', robots permission=' + str(allowed) + ', nofollow=' + str(is_nofollow))
				return None, False, 0

	def search_encoding(self, headers, code):
		"""Searche encoding of webpage in source code

		If an encoding is found in source code, score is .5, but if not
		score is 0 and encoding is utf-8.

		:param headers: hearders of requests
		:type headers: dict
		:param code: source code
		:type code: str
		:return: encoding of webpage and it score

		"""
		# search in headers :
		headers = str(headers).lower()
		charset = headers.find('charset')
		end_charset = headers.find('\'', charset)
		if charset != -1 and end_charset != -1:
			return headers[charset+8:end_charset], .5
		else:
			# search in source code:
			self.parser_encoding.feed(code)
			if self.parser_encoding.encoding is not None:
				return self.parser_encoding.encoding, .5
			else:
				speak('No encoding', 9)
				return 'utf-8', 0

	def is_nofollow(self, url):
		"""Check if take links

		:param url: webpage url
		:type url: str
		:return: true if nofollow and url

		"""
		if url.endswith('!nofollow!'):
			return True, url[:-10]
		else:
			return False, url

	def check_robots_perm(self, url):
		"""Check robots.txt for permission

		:param url: webpage url
		:type url: str
		:return: true if can crawl

		"""
		try:
			allowed = self.reqrobots.allowed(url, USER_AGENT)
		except ServerError as error:
			speak('Error robots.txt (reppy): ' + str(error) + ' ' + url, 24)
			allowed = True
		except requests.exceptions.Timeout:
			speak('Error robots.txt (timeout): ' + url)
			allowed = True
		except requests.exceptions.RequestException as error:
			speak('Error robots.txt (requests): ' + str(error) + ' ' + url, 24)
			allowed = True
		except Exception as error:
			speak('Unknow robots.txt error: ' + str(error) + ' ' + url, 24)
			allowed = True
		return allowed

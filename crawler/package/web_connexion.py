#!/usr/bin/python3

"""Connexion to webpage are manage with requests module.
Thoses errors are waiting for: timeout with socket module and with urllib3 mudule
and all RequestException errors."""

import requests
from urllib.parse import urlparse

from reppy.cache import RobotsCache
from reppy.exceptions import ServerError

from package.data import USER_AGENT, HEADERS, TIMEOUT
from package.module import speak, no_connexion, is_nofollow
from package.parsers import Parser_encoding

class WebConnexion(object):
	"""Manage the web connexion with the page to crawl."""
	def __init__(self):
		self.reqrobots = RobotsCache()
		self.parser_encoding = Parser_encoding()


	def get_code(self, url):
		"""Get source code of given url.

		:param url: url of webpage
		:type url: str
		:return: source code, True if no take links, score and new url (redirection)
		"""
		nofollow, url = is_nofollow(url)
		try:
			request = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
		except requests.packages.urllib3.exceptions.ReadTimeoutError:
			speak('Read timeout rrror (urllib3): ' + url, 7)
			return None, False, 0, None
		except requests.exceptions.Timeout:
			speak('Timeout error: ' + url, 7)
			return None, False, 0, None
		except requests.exceptions.RequestException as error:
			speak('Connexion failed: {}, {}'.format(str(error), url), 8)
			if no_connexion():
				return 'no connexion', None, 0, None
			else:
				return None, False, 0, None
		else:
			allowed = self.check_robots_perm(url)
			if request.status_code == requests.codes.ok and request.headers.get('Content-Type', '').startswith('text/html') and	allowed:
				# Search encoding of webpage:
				request.encoding, score = self.search_encoding(request.headers, request.text)
				url = self.param_duplicate(request)
				return request.text, nofollow, score, url
			else:
				speak('Webpage infos: status code=' + str(request.status_code) + ', Content-Type=' + \
					request.headers.get('Content-Type', '') + ', robots perm=' + str(allowed))
				return 'ignore', False, 0, request.url


	def search_encoding(self, headers, code):
		"""Searche encoding of webpage in source code.

		If an encoding is found in source code, score is .5, but if not
		score is 0 and encoding is utf-8.

		:param headers: hearders of requests
		:type headers: dict
		:param code: source code
		:type code: str
		:return: encoding of webpage and it score
		"""
		# Search in headers:
		headers = str(headers).lower()
		charset = headers.find('charset')
		end_charset = headers.find('\'', charset)
		if charset != -1 and end_charset != -1:
			return headers[charset+8:end_charset], 1
		else:
			# Search in source code:
			self.parser_encoding.feed(code)
			if self.parser_encoding.encoding != '':
				return self.parser_encoding.encoding, 1
			else:
				speak('No encoding', 9)
				return 'utf-8', 0


	def check_robots_perm(self, url):
		"""Check robots.txt for permission.

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


	def param_duplicate(self, request):
		"""Avoid param duplicate.

		:param request: request
		:type request: requests.models.Response
		:return: url
		"""
		infos_url = urlparse(request.url)
		if infos_url.query != '':
			size_with_param = len(request.text)
			print(size_with_param)
			new_url = infos_url.scheme + '://' + infos_url.netloc + infos_url.path
			print(new_url)
			size_without_param = len(requests.get(new_url).text)
			print(size_without_param)
			if size_with_param == size_without_param:
				return new_url
			else:
				return request.url
		else:
			return request.url

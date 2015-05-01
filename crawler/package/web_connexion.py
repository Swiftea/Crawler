#!/usr/bin/python3

"""Connexion to webpage are manage with requests module.
Thoses errors are waiting for: timeout with socket module and with urllib3 mudule
and all RequestException errors."""

import requests
from urllib.parse import urlparse

from reppy.cache import RobotsCache
from reppy.exceptions import ServerError

from package.data import USER_AGENT, HEADERS, TIMEOUT
from package.module import tell, no_connexion, is_nofollow, clean_link
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
			tell('Read timeout error (urllib3): ' + url, 3)
			return None, False, 0, None
		except requests.exceptions.Timeout:
			tell('Timeout error: ' + url, 4)
			return None, False, 0, None
		except requests.exceptions.RequestException as error:
			tell('Connexion failed: {}, {}'.format(str(error), url), 5)
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
				if url:  # Redirected url don't pass in clean_link, too many params or too long.
					return request.text, nofollow, score, url
				else:
					return 'ignore', False, 0, None
			else:
				tell('Webpage infos: status code=' + str(request.status_code) + ', Content-Type=' + \
					request.headers.get('Content-Type', '') + ', robots perm=' + str(allowed), severity=0)
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
				tell('No encoding', 9, severity=0)
				return 'utf-8', 0

	def check_robots_perm(self, url):
		"""Check robots.txt for permission.

		:param url: webpage url
		:type url: str
		:return: True if can crawl

		"""
		try:
			allowed = self.reqrobots.allowed(url, USER_AGENT)
		except ServerError as error:
			tell('Error robots.txt (reppy): ' + str(error) + ' ' + url, 6)
			allowed = True
		except requests.exceptions.Timeout:
			tell('Error robots.txt (timeout): ' + url)
			allowed = True
		except requests.exceptions.RequestException as error:
			tell('Error robots.txt (requests): ' + str(error) + ' ' + url, 7)
			allowed = True
		except Exception as error:
			tell('Unknow robots.txt error: ' + str(error) + ' ' + url, 8)
			allowed = True
		return allowed

	def param_duplicate(self, request):
		"""Avoid param duplicate.

		Compare the size of source code with params and whitout.
		Return url whitout params if it's the smae size.

		:param request: request
		:type request: requests.models.Response
		:return: url

		"""
		infos_url = urlparse(request.url)
		if infos_url.query != '':
			size_with_param = len(request.text)
			new_url = infos_url.scheme + '://' + infos_url.netloc + infos_url.path
			size_without_param = len(requests.get(new_url).text)
			if size_with_param == size_without_param:
				return clean_link(new_url)
			else:
				return clean_link(request.url)
		else:
			return clean_link(request.url)

#!/usr/bin/env python3

"""Connection to webpage is managed by requests module.
Those errors are waiting for: timeout with socket module and urllib3 module and all RequestException errors."""

import requests
from urllib.parse import urlparse

from reppy.cache import RobotsCache
from reppy.exceptions import ServerError


from crawler.swiftea_bot.data import USER_AGENT, HEADERS, TIMEOUT
from crawler.swiftea_bot.module import tell, remove_duplicates
from crawler.crawling import parsers, data_processing
from crawler.crawling.searches import clean_link


class WebConnection(object):
	"""Manage the web connection with the page to crawl."""
	def __init__(self):
		self.reqrobots = RobotsCache(capacity=100)
		self.parser_encoding = parsers.ExtractEncoding()

	def get_code(self, url):
		"""Get source code of given url.

		:param url: url of webpage
		:type url: str
		:return: source code, True if no take links, score and new url (redirection)

		"""
		nofollow, url = data_processing.is_nofollow(url)
		result = self.send_request(url)
		if not isinstance(result, requests.models.Response):
			return None, result, None, None, url
		else:
			request = result
			del result
			allowed = self.check_robots_perm(url)
			if request.status_code == requests.codes.ok and request.headers.get('Content-Type', '').startswith('text/html') and	allowed:
				# Search encoding of webpage:
				request.encoding, score = self.search_encoding(request.headers, request.text)
				new_url, code = self.duplicate_content(request, url)  # new_url is clean and maybe without params
				all_urls = data_processing.all_urls(request)  # List of urls to delete
				if new_url in all_urls:  # new_url don't be delete
					all_urls.remove(new_url)
				return new_url, code, nofollow, score, all_urls
			else:
				tell('Webpage infos: status code=' + str(request.status_code) + ', Content-Type=' + \
					request.headers.get('Content-Type', '') + ', robots perm=' + str(allowed), severity=0)
				# All redirections urls, the first and the last:
				all_urls = data_processing.all_urls(request)
				all_urls.append(request.url)
				all_urls.append(url)
				return None, 'ignore', None, None, remove_duplicates(all_urls)

	def send_request(self, url):
		try:
			request = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
		except requests.packages.urllib3.exceptions.ReadTimeoutError:
			tell('Read timeout error (urllib3): ' + url, 3)
			return None
		except requests.exceptions.Timeout:
			tell('Timeout error: ' + url, 4)
			return None
		except (requests.exceptions.RequestException, requests.exceptions.ConnectionError) as error:
			tell('Connection failed: {}, {}'.format(str(error), url), 5)
			if data_processing.check_connection():
				return None
			else:
				return 'no connection'
		except UnicodeDecodeError as error:
			tell('UnicodeDecodeError: ' + str(error))
		else:
			return request

	def search_encoding(self, headers, code):
		"""Search encoding of webpage in source code.

		If an encoding is found in source code, score is 1, but if not
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
		else:
			return allowed

	def duplicate_content(self, request1, url):
		"""Avoid param duplicate.

		Compare source codes with params and whitout.
		Return url whitout params if it's the same content.

		:param request: request
		:type request: requests.models.Response
		:return: url, source code

		"""
		url1 = clean_link(request1.url)
		if url1 is None:
			return url, request1.text
		infos_url = urlparse(url1)
		if infos_url.query != '':
			new_url = infos_url.scheme + '://' + infos_url.netloc + infos_url.path
			request2 = self.send_request(new_url)
			if not isinstance(request2, requests.models.Response):
				return url1, request1.text
			request2.encoding = self.search_encoding(request2.headers, request2.text)[0]
			url2 = clean_link(request2.url)
			if url2 is None:
				return url1, request1.text
			if data_processing.duplicate_content(request1.text, request2.text):
				tell("Same content: " + url1 + " and " + url2)   # Tests
				return url2, request2.text
			else:
				return url1, request1.text
		else:
			return url1, request1.text

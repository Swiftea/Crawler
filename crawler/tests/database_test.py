#!/usr/bin/env python3

from crawler.database import database
from crawler.tests.test_data import URL


class DatabaseBaseTest:
	"""Base class for all crawler test classes."""
	def setup_method(self, _):
		self.url = URL
		self.url_secure = 'https://aetfiws.ovh'


class TestDatabase(DatabaseBaseTest):
	def test_url_is_secure(self):
		assert database.url_is_secure(self.url) is False
		assert database.url_is_secure(self.url_secure)

	def test_convert_secure(self):
		assert database.convert_secure(self.url) == self.url_secure
		assert database.convert_secure(self.url_secure) == self.url

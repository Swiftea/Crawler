#!/usr/bin/env python3

from database.database import *
from tests.test_data import URL


class DatabaseBaseTest(object):
	"""Base class for all crawler test classes."""
	def setup_method(self, _):
		self.url = URL
		self.url_secure = 'https://aetfiws.ovh'


class TestDatabase(DatabaseBaseTest):
	def test_url_is_secure(self):
		assert url_is_secure(self.url) == False
		assert url_is_secure(self.url_secure) == True

	def test_convert_secure(self):
		assert convert_secure(self.url) == self.url_secure
		assert convert_secure(self.url_secure) == self.url

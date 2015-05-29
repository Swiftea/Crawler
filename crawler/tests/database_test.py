#!/usr/bin/python3

from database.database import *
from tests.test_data import URL

class DatabaseBaseTest(object):
	"""Base class for all crawler test classes."""
	def setup_method(self, _):
		self.url = URL
		self.secure = 'https://aetfiws.alwaysdata.net'

class TestDatabase(DatabaseBaseTest):
	def test_url_is_secure(self):
		assert url_is_secure(self.url) == False
		assert url_is_secure(self.secure) == True

	def test_convert_secure(self):
		assert convert_secure(self.url) == self.secure
		assert convert_secure(self.secure) == self.url

#!/usr/bin/python3

import sys
from configparser import ConfigParser
from os import mkdir, remove, path


from main import Crawler
from swiftea_bot.data import DIR_LINKS, FILE_CONFIG, MAX_LINKS, FILE_BASELINKS, DIR_CONFIG
from swiftea_bot.module import create_dirs
from tests.test_data import reset, BASE_LINKS
import swiftea_bot.private_data as pvdata
from database.database_swiftea import DatabaseSwiftea


class TestGlobalTest:
	def test_RedirectOutput(self):
		sys.stdout = RedirectOutput('test_RedirectOutput.ext')
		print('A test message')

class RedirectOutput(object):
	def __init__(self, file):
		self.output = open(file, 'w')

	def write(self, text):
		self.output.write(text)
		self.output.flush()

class TestLocal(object):
	def test_insert(self):
		infos = {
	        'title': 'un titre',
	        'description': 'une tres longue description',
	        'url': 'http://une.url.bidon.truc',
	        'language': 'fr',
	        'score': '1',
	        'homepage': '1',
	        'sanesearch': '1',
	        'favicon': 'http://une.url.bidon.truc/favicon.ico',
	    }
		database_swiftea = DatabaseSwiftea(pvdata.HOST_DB, pvdata.USER_DB,
	        pvdata.PASSWORD_DB, pvdata.NAME_DB, pvdata.NAME_TABLE)
		response = database_swiftea.send_command(
		"""INSERT INTO website (title, description, url, first_crawl, last_crawl, language,
		popularity, score, homepage, sanesearch, favicon)
		VALUES (%s, %s, %s, NOW(), NOW(), %s, 1, %s, %s, %s, %s)""",
		(infos['title'][:254], infos['description'], infos['url'], infos['language'],
		infos['score'], infos['homepage'], infos['sanesearch'], infos['favicon']))
		assert response == (None, [0, 'Send command: ok'])

class TestGlobal(object):
	def _test_crawler(self):
		defstdout = sys.__stdout__
		defstderr = sys.__stderr__
		sys.stdout = RedirectOutput('log')
		sys.stderr = RedirectOutput('err')
		create_dirs()
		if not path.exists(DIR_LINKS): mkdir(DIR_LINKS)
		with open(FILE_BASELINKS, 'w') as myfile:
			myfile.write(BASE_LINKS)
		crawler = Crawler()
		crawler.database.set_name('swiftea_tests')
		crawler.sftp_manager.set_sftp_index('html/data/test_index')
		config = ConfigParser()
		config['DEFAULT'] = {
			'run': 'false',
			'reading_file_number': '0',
			'writing_file_number': '1',
			'reading_line_number': '0',
			'max_links': MAX_LINKS
		}
		with open(FILE_CONFIG, 'w') as configfile:
			config.write(configfile)
		crawler.start()

		crawler.send_inverted_index()

		reset()
		sys.stdout = defstdout
		sys.stderr = defstderr
		remove('log')
		remove('err')

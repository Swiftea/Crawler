#!/usr/bin/python3

import sys
from configparser import ConfigParser
from os import mkdir, remove

from main import Crawler
from swiftea_bot.data import DIR_LINKS, FILE_CONFIG, MAX_LINKS, FILE_BASELINKS, DIR_CONFIG
from swiftea_bot.module import create_dirs, create_doc
from tests.test_data import reset, BASE_LINKS

class RedirectOutput(object):
	def __init__(self, file):
		self.output = open(file, 'w')

	def write(self, text):
		self.output.write(text)
		self.output.flush()


class TestGlobal(object):
	def test_crawler(self):
		defstdout = sys.__stdout__
		defstderr = sys.__stderr__
		sys.stdout = RedirectOutput('log')
		sys.stderr = RedirectOutput('err')
		create_dirs()
		create_doc()
		mkdir(DIR_LINKS)
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

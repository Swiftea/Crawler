#!/usr/bin/env python3

from shutil import rmtree
from os import mkdir, path
import json


from swiftea_bot import data
from swiftea_bot.module import *
from swiftea_bot.file_manager import *
from tests.test_data import URL, INVERTED_INDEX, BASE_LINKS
import swiftea_bot.links


def test_create_dirs():
	create_dirs()


def test_tell():
	tell('Simple message', 0)
	tell('Hard message', severity=2)


def test_is_index():
	assert is_index() == False
	open(data.FILE_INDEX, 'w').close()
	assert is_index() == True


def test_remove_duplicates():
	assert remove_duplicates(['word', 'word']) == ['word']


def test_stats_webpages():
	stats_webpages(100, 1200)


class SwifteaBotBaseTest:
	def setup_method(self, _):
		self.crawl_option = {'domaine': 'idesys.org', 'level': 3, 'sub-domaine': True}
		self.url = URL
		self.inverted_index = INVERTED_INDEX
		self.links = ['http://aetfiws.ovh/page.php', 'http://aetfiws.ovh',
			'http://aetfiws.ovh?w=word', 'http://aetfiws.ovh/page1']
		self.max_links = 3
		self.reading_line_number = 0
		self.config = ConfigParser()
		self.run = 'true'
		self.max_size_file = 2

		self.c1 = [
	        {'domaine': '', 'level': -1, 'completed': 0},
	        {'domaine': '', 'level': -1, 'completed': 0},
	        {'domaine': 'idesys.org', 'level': 0, 'completed': 0},
	        {'domaine': 'idesys.org', 'level': 1, 'completed': 0},
	        {'domaine': 'polytech.fr', 'level': 0, 'completed': 0},
	        {'domaine': 'idesys.org', 'level': 2, 'completed': 0}
	    ]
		self.c2 = [
	        {'domaine': '', 'level': -1, 'completed': 0},
	        {'domaine': '', 'level': -1, 'completed': 0},
	        {'domaine': 'idesys.org', 'level': 0, 'completed': 0},
	        {'domaine': 'idesys.org', 'level': 1, 'completed': 0},
	        {'domaine': 'polytech.fr', 'level': 0, 'completed': 0},
	        {'domaine': 'idesys.org', 'level': 2, 'completed': 0},
	        {'domaine': 'polytech.fr', 'level': 1, 'completed': 0}
	    ]
		self.c3 = [
	        {'domaine': '', 'level': -1, 'completed': 0},
	        {'domaine': '', 'level': -1, 'completed': 0},
	        {'domaine': 'idesys.org', 'level': 0, 'completed': 0},
	        {'domaine': 'idesys.org', 'level': 1, 'completed': 0},
	        {'domaine': 'polytech.fr', 'level': 0, 'completed': 0},
	        {'domaine': 'idesys.org', 'level': 2, 'completed': 0},
	        {'domaine': 'polytech.fr', 'level': 1, 'completed': 0},
	        {'domaine': '', 'level': -1, 'completed': 0},
	    ]


class TestModule(SwifteaBotBaseTest):
	def test_can_add_doc(self):
		docs = [{'url': self.url}]
		assert can_add_doc(docs, {'url': self.url}) == False
		assert can_add_doc(docs, {'url': self.url + '/page'}) == True


class TestFileManager(SwifteaBotBaseTest):
	def test_init(self):
		FileManager.__init__(self, {})
		FileManager.__init__(self, {})

	def test_check_stop_crawling(self):
		FileManager.check_stop_crawling(self)
		assert self.run == 'true'

	def test_save_config(self):
		FileManager.save_config(self)

	def test_save_links(self):
		if not path.exists(data.DIR_LINKS):
			mkdir(data.DIR_LINKS)
		FileManager.save_links(self, BASE_LINKS.split())
		links = ['http://www.planet-libre.org', 'http://www.actu-environnement.com', 'http://a.fr']
		links.extend(BASE_LINKS.split())
		FileManager.save_links(self, links)

	def test_check_size_files(self):
		FileManager.check_size_files(self)
		self.max_size_file = 1
		tell('Simple message')
		tell('Simple message')
		FileManager.check_size_files(self)
		tell('Simple message')
		tell('Simple message')
		FileManager.check_size_files(self)

	def test_get_url(self):
		with open(data.DIR_LINKS + '0', 'w') as myfile:
			myfile.write(self.url + '\nhttp://example.en/page qui parle de ça')
		assert FileManager.get_url(self) == (self.url, False)
		assert FileManager.get_url(self) == ('http://example.en/page qui parle de ça', True)
		assert FileManager.get_url(self) == 'error'

	def test_save_inverted_index(self):
		FileManager.save_inverted_index(self, self.inverted_index)

	def test_get_inverted_index(self):
		assert FileManager.get_inverted_index(self) == self.inverted_index

	def test_read_inverted_index(self):
		mkdir('data/inverted_index/FR')
		mkdir('data/inverted_index/FR/A/')
		with open('data/inverted_index/FR/A/ab.sif', 'w') as myfile:
			myfile.write('{"abondamment": {"1610": 0.005618}}')
		inverted_index = FileManager.read_inverted_index(self)
		assert inverted_index == {'FR': {'A': {'ab': {'abondamment': {1610: 0.005618}}}}}

	def test_get_lists_words(self):
		# No dirs badwords and stopwords
		stopwords, badwords = FileManager.get_lists_words(self)
		# Dirs created
		with open(data.DIR_DATA + 'stopwords/' + 'en.stopwords.txt', 'w') as myfile:
			myfile.write('then\nalready')
		with open(data.DIR_DATA + 'badwords/' + 'en.badwords.txt', 'w') as myfile:
			myfile.write('verybadword')
		stopwords, badwords = FileManager.get_lists_words(self)
		assert stopwords == {'en': ['then', 'already']}
		assert badwords == {'en': ['verybadword']}

	def test_link_get_filename(self):
		r00, s00, d00, r00_ = swiftea_bot.links.get_filename(
			[], {'domaine': '', 'level': -1}
		)
		assert r00 == 0
		assert s00 == True
		assert d00 == [
			{'domaine': '', 'level': -1, 'completed': 0},
		]
		assert r00_ == -1

		r0, s0, d0, r0_ = swiftea_bot.links.get_filename(
			[], {'domaine': 'idesys.org', 'level': 2}
		)
		assert r0 == 0
		assert s0 == True
		assert d0 == [
			{'domaine': 'idesys.org', 'level': 2, 'completed': 0},
			{'domaine': '', 'level': -1, 'completed': 0}
		]
		assert r0_ == 1

		r1, s1, d1, r1_ = swiftea_bot.links.get_filename(
			self.c1, {'domaine': 'idesys.org', 'level':	2}
		)
		assert r1 == 5
		assert s1 == False
		assert d1 == self.c1
		assert r1_ == 1

		with open(data.DIR_LINKS + '1', 'w') as link_file:
			link_file.write('http://swiftea.fr\n')

		r2, s2, d2, r2_ = swiftea_bot.links.get_filename(
			self.c1, {'domaine': '', 'level': -1}
		)
		assert r2 == 1
		assert s2 == False
		assert d2 == self.c1
		assert r2_ == -1

		r3, s3, d3, r3_ = swiftea_bot.links.get_filename(
			self.c1, {'domaine': 'polytech.fr', 'level': 1}
		)
		assert r3 == 6
		assert s3 == True
		assert d3 == self.c2
		assert r3_ == 1

		r4, s4, d4, r4_ = swiftea_bot.links.get_filename(
			self.c1, {'domaine': '', 'level': -1}
		)
		assert r4 == 1
		assert s4 == False
		assert d4 == self.c2
		assert r4_ == -1

		r5, s5, d5, r5_ = swiftea_bot.links.get_filename(
			self.c1, {'domaine': '', 'level': -1}, 2
		)
		assert r5 == 7
		assert s5 == True
		assert d5 == self.c3
		assert r5_ == -1

	def test_link_save_links(self):
		links = ['http://idesys.org/index.html']
		with open(data.FILE_LINKS, 'w') as json_file:
			json.dump(self.c1, json_file)
		swiftea_bot.links.save_links(
			links, {'domaine': 'polytech.fr', 'level': 1, 'sub-domaine': True}
		)

	def test_links_get_level(self):
		assert swiftea_bot.links.get_level('idesys.org') == 2
		assert swiftea_bot.links.get_level('') == -1
		assert swiftea_bot.links.get_level('swiftea.fr') == 0

	def test_links_filter_links(self):
		links = ['http://idesys.org', 'http://idesys.org/jehmaker',
			'http://polytech.fr', 'http://beta.idesys.org']

		l1, l1_ = swiftea_bot.links.filter_links(
			links, {'domaine': 'idesys.org', 'level': 1, 'sub-domaine': True})
		assert l1 == ['http://idesys.org', 'http://idesys.org/jehmaker',
			'http://beta.idesys.org']
		assert l1_ == ['http://polytech.fr']

		l2, l2_ = swiftea_bot.links.filter_links(
			links, {'domaine': 'idesys.org', 'level': 1, 'sub-domaine': False}
		)
		assert l2 == ['http://idesys.org', 'http://idesys.org/jehmaker']
		assert l2_ == ['http://polytech.fr', 'http://beta.idesys.org']

		l2 = swiftea_bot.links.filter_links(
			links, {'domaine': '', 'level': -1, 'sub-domaine': False}
		)
		assert l2 == links

#!/usr/bin/env python3

from shutil import rmtree
from os import mkdir, path
import json


from crawler.swiftea_bot import data
from crawler.swiftea_bot import module
from crawler.swiftea_bot import file_manager
from crawler.tests.test_data import URL, INVERTED_INDEX, BASE_LINKS
from crawler.swiftea_bot import links as swiftea_bot_links


def test_create_dirs():
	module.create_dirs()


def test_tell():
	module.tell('Simple message', 0)
	module.tell('Hard message', severity=2)


def test_is_index():
	assert module.is_index() == False
	open(data.FILE_INDEX, 'w').close()
	assert module.is_index() == True


def test_remove_duplicates():
	assert module.remove_duplicates(['word', 'word']) == ['word']


def test_stats_webpages():
	module.stats_webpages(100, 1200)


class SwifteaBotBaseTest:
	def setup_method(self, _):
		self.crawl_option = {'domain': 'idesys.org', 'level': 3, 'sub-domain': True}
		self.url = URL
		self.inverted_index = INVERTED_INDEX
		self.links = ['http://aetfiws.ovh/page.php', 'http://aetfiws.ovh',
			'http://aetfiws.ovh?w=word', 'http://aetfiws.ovh/page1']
		self.max_links = 3
		self.reading_line_number = 0
		self.config = file_manager.ConfigParser()
		self.run = 'true'
		self.max_size_file = 2

		self.c1 = [
	        {'domain': '', 'level': -1, 'completed': 0},
	        {'domain': '', 'level': -1, 'completed': 0},
	        {'domain': 'idesys.org', 'level': 0, 'completed': 0},
	        {'domain': 'idesys.org', 'level': 1, 'completed': 0},
	        {'domain': 'polytech.fr', 'level': 0, 'completed': 0},
	        {'domain': 'idesys.org', 'level': 2, 'completed': 0}
	    ]
		self.c2 = [
	        {'domain': '', 'level': -1, 'completed': 0},
	        {'domain': '', 'level': -1, 'completed': 0},
	        {'domain': 'idesys.org', 'level': 0, 'completed': 0},
	        {'domain': 'idesys.org', 'level': 1, 'completed': 0},
	        {'domain': 'polytech.fr', 'level': 0, 'completed': 0},
	        {'domain': 'idesys.org', 'level': 2, 'completed': 0},
	        {'domain': 'polytech.fr', 'level': 1, 'completed': 0}
	    ]
		self.c3 = [
	        {'domain': '', 'level': -1, 'completed': 0},
	        {'domain': '', 'level': -1, 'completed': 0},
	        {'domain': 'idesys.org', 'level': 0, 'completed': 0},
	        {'domain': 'idesys.org', 'level': 1, 'completed': 0},
	        {'domain': 'polytech.fr', 'level': 0, 'completed': 0},
	        {'domain': 'idesys.org', 'level': 2, 'completed': 0},
	        {'domain': 'polytech.fr', 'level': 1, 'completed': 0},
	        {'domain': '', 'level': -1, 'completed': 0},
	    ]


class TestModule(SwifteaBotBaseTest):
	def test_can_add_doc(self):
		docs = [{'url': self.url}]
		assert module.can_add_doc(docs, {'url': self.url}) == False
		assert module.can_add_doc(docs, {'url': self.url + '/page'}) == True


class TestFileManager(SwifteaBotBaseTest):
	def test_init(self):
		file_manager.FileManager.__init__(self, {})
		file_manager.FileManager.__init__(self, {})

	def test_check_stop_crawling(self):
		file_manager.FileManager.check_stop_crawling(self)
		assert self.run == 'true'

	def test_save_config(self):
		file_manager.FileManager.save_config(self)

	def test_save_links(self):
		if not path.exists(data.DIR_LINKS):
			mkdir(data.DIR_LINKS)
		file_manager.FileManager.save_links(self, BASE_LINKS.split())
		links = ['http://www.planet-libre.org', 'http://www.actu-environnement.com', 'http://a.fr']
		links.extend(BASE_LINKS.split())
		file_manager.FileManager.save_links(self, links)

	def test_check_size_files(self):
		file_manager.FileManager.check_size_files(self)
		self.max_size_file = 1
		module.tell('Simple message')
		module.tell('Simple message')
		file_manager.FileManager.check_size_files(self)
		module.tell('Simple message')
		module.tell('Simple message')
		file_manager.FileManager.check_size_files(self)

	# def test_get_url(self):
	# 	with open(data.DIR_LINKS + '0', 'w') as myfile:
	# 		myfile.write(self.url + '\nhttp://example.en/page qui parle de ça')
	# 	assert file_manager.FileManager.get_url(self) == (self.url, False)
	# 	assert file_manager.FileManager.get_url(self) == ('http://example.en/page qui parle de ça', True)
	# 	assert file_manager.FileManager.get_url(self) == 'error'

	def test_save_inverted_index(self):
		file_manager.FileManager.save_inverted_index(self, self.inverted_index)

	def test_get_inverted_index(self):
		assert file_manager.FileManager.get_inverted_index(self) == self.inverted_index

	def test_read_inverted_index(self):
		# mkdir('data/inverted_index/FR')
		if not path.exists('inverted_index/FR'):
			mkdir('inverted_index/FR')
		# mkdir('data/inverted_index/FR/A/')
		if not path.exists('inverted_index/FR/A'):
			mkdir('inverted_index/FR/A/')
		# with open('data/inverted_index/FR/A/ab.sif', 'w') as myfile:
		with open('inverted_index/FR/A/ab.sif', 'w') as myfile:
			myfile.write('{"abondamment": {"1610": 0.005618}}')
		inverted_index = file_manager.FileManager.read_inverted_index(self)
		assert inverted_index == {'FR': {'A': {'ab': {'abondamment': {1610: 0.005618}}}}}

	def test_get_lists_words(self):
		# No dirs badwords and stopwords
		stopwords, badwords = file_manager.FileManager.get_lists_words(self)
		# Dirs created
		with open('stopwords/' + 'en.stopwords.txt', 'w') as myfile:
			myfile.write('then\nalready')
		with open('badwords/' + 'en.badwords.txt', 'w') as myfile:
			myfile.write('verybadword')
		stopwords, badwords = file_manager.FileManager.get_lists_words(self)
		assert stopwords == {'en': ['then', 'already']}
		assert badwords == {'en': ['verybadword']}

	def test_link_get_filename(self):
		r00, s00, d00, r00_ = swiftea_bot_links.get_filename(
			[], {'domain': '', 'level': -1}
		)
		assert r00 == 0
		assert s00 == True
		assert d00 == [
			{'completed': 0, 'domain': '', 'file': 0, 'level': -1, 'line': 1}
		]
		assert r00_ == -1

		r0, s0, d0, r0_ = swiftea_bot_links.get_filename(
			[], {'domain': 'idesys.org', 'level': 2}
		)
		assert r0 == 0
		assert s0 == True
		assert d0 == [
			{'completed': 0, 'domain': 'idesys.org', 'file': 0, 'level': 2, 'line': 1},
			{'completed': 0, 'domain': 'idesys.org', 'file': 1, 'level': 3, 'line': 1}
		]
		assert r0_ == 1

		r1, s1, d1, r1_ = swiftea_bot_links.get_filename(
			self.c1, {'domain': 'idesys.org', 'level':	2}
		)
		assert r1 == 5
		# assert s1 == False
		assert d1 == self.c1
		# assert r1_ == 1

		with open(data.DIR_LINKS + '1', 'w') as link_file:
			link_file.write('http://swiftea.fr\n')

		r2, s2, d2, r2_ = swiftea_bot_links.get_filename(
			self.c1, {'domain': '', 'level': -1}
		)
		assert r2 == 1
		assert s2 == False
		assert d2 == self.c1
		assert r2_ == -1

		r3, s3, d3, r3_ = swiftea_bot_links.get_filename(
			self.c1, {'domain': 'polytech.fr', 'level': 1}
		)
		# assert r3 == 6
		assert s3 == True
		# assert d3 == self.c2
		# assert r3_ == 1

		r4, s4, d4, r4_ = swiftea_bot_links.get_filename(
			self.c1, {'domain': '', 'level': -1}
		)
		assert r4 == 1
		assert s4 == False
		# assert d4 == self.c2
		assert r4_ == -1

		r5, s5, d5, r5_ = swiftea_bot_links.get_filename(
			self.c1, {'domain': '', 'level': -1}, 2
		)
		# assert r5 == 7
		assert s5 == True
		# assert d5 == self.c3
		assert r5_ == -1

	def test_link_save_links(self):
		links = ['http://idesys.org/index.html']
		with open(data.FILE_LINKS, 'w') as json_file:
			json.dump(self.c1, json_file)
		swiftea_bot_links.save_links(
			links, {'domain': 'polytech.fr', 'level': 1, 'sub-domain': True}
		)

	def test_links_filter_links(self):
		links = ['http://idesys.org', 'http://idesys.org/jehmaker',
			'http://polytech.fr', 'http://beta.idesys.org']

		l1, l1_ = swiftea_bot_links.filter_links(
			links, {'domain': 'idesys.org', 'level': 1, 'sub-domain': True})
		assert l1 == ['http://idesys.org', 'http://idesys.org/jehmaker',
			'http://beta.idesys.org']
		assert l1_ == ['http://polytech.fr']

		l2, l2_ = swiftea_bot_links.filter_links(
			links, {'domain': 'idesys.org', 'level': 1, 'sub-domain': False}
		)
		assert l2 == ['http://idesys.org', 'http://idesys.org/jehmaker']
		assert l2_ == ['http://polytech.fr', 'http://beta.idesys.org']

		l2 = swiftea_bot_links.filter_links(
			links, {'domain': '', 'level': -1, 'sub-domain': False}
		)
		assert l2 == (links, [])

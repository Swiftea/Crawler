#!/usr/bin/python3

from shutil import rmtree
from os import mkdir
import swiftea_bot.data
from swiftea_bot.module import *
from swiftea_bot.file_manager import *
from tests.test_data import URL, INVERTED_INDEX, BASE_LINKS

class SwifteaBotBaseTest(object):
	def setup_method(self, _):
		self.url = URL
		self.inverted_index = INVERTED_INDEX
		self.links = ['http://aetfiws.alwaysdata.net/page.php', 'http://aetfiws.alwaysdata.net',
			'http://aetfiws.alwaysdata.net?w=word', 'http://aetfiws.alwaysdata.net/page1']
		self.max_links = 3
		self.reading_file_number = 1
		self.writing_file_number = 5
		self.reading_line_number = 0
		self.config = ConfigParser()
		self.run = 'true'


class TestModule(SwifteaBotBaseTest):
	def test_create_dirs(self):
		create_dirs()

	def test_create_doc(self):
		create_doc()
		create_doc()
		with open(swiftea_bot.data.FILE_DOC, 'w') as myfile:
			myfile.write('This is not the doc.')
		create_doc()

	def test_tell(self):
		tell('A test message', 0)
		tell('Big test', severity=2)

	def test_is_index(self):
		assert is_index() == False
		open(FILE_INDEX, 'w').close()
		assert is_index() == True

	def test_can_add_doc(self):
		docs = [{'url': self.url}]
		assert can_add_doc(docs, {'url': self.url}) == False
		assert can_add_doc(docs, {'url': self.url + '/page'}) == True

	def test_remove_duplicates(self):
		assert remove_duplicates(['word', 'word']) == ['word']

	def test_stats_webpages(self):
		stats_webpages(100, 1200)

class TestFileManager(SwifteaBotBaseTest):
	def test_init(self):
		FileManager.__init__(self)
		FileManager.__init__(self)

	def test_check_stop_crawling(self):
		FileManager.check_stop_crawling(self)
		assert self.run == 'true'

	def test_get_max_links(self):
		FileManager.get_max_links(self)
		assert self.max_links == MAX_LINKS

	def test_save_config(self):
		FileManager.save_config(self)

	def test_save_links(self):
		mkdir(DIR_LINKS)
		FileManager.save_links(self, BASE_LINKS.split())
		FileManager.save_links(self, BASE_LINKS[5:].split())

	def test_get_url(self):
		with open(DIR_LINKS + '1', 'w') as myfile:
			myfile.write(self.url + '\nhttp://example.en/page qui parle de ça')
		assert FileManager.get_url(self) == self.url
		assert FileManager.get_url(self) == 'http://example.en/page qui parle de ça'
		self.reading_file_number = 1
		assert FileManager.get_url(self) == 'stop'

	def test_ckeck_size_links(self):
		self.max_links = 2
		FileManager.ckeck_size_links(self, self.links)

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

	def test_save_docs(self):
		FileManager.save_docs(self, [{'url': self.url}])
		FileManager.save_docs(self, [])

	def test_get_docs(self):
		assert FileManager.get_docs(self) == [{'url': self.url}]
		assert FileManager.get_docs(self) == []
		#rmtree('data')

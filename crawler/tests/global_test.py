#!/usr/bin/python3

"""Classes to test Swiftea-Crawler globaly."""

from os import mkdir
from configparser import ConfigParser

import package.data as data
from main import Crawler
from package.module import speak, create_dirs, create_doc
from package.web_connexion import WebConnexion
from package.database_swiftea import DatabaseSwiftea
from package.inverted_index import InvertedIndex
from package.ftp_swiftea import FTPSwiftea
from package.searches import SiteInformations
from package.file_manager import FileManager
import tests.tests_data as tests_data

def def_links():
    with open(data.DIR_LINKS + '0', 'w') as myfile:
        myfile.write(tests_data.base_links)


class TestDatabaseSwiftea(DatabaseSwiftea):

    suggestions = tests_data.suggestions

    def __init__(self, host, user, password, name):
        DatabaseSwiftea.__init__(self, host, user, password, name)

    def send_infos(self, infos):
        assert infos == tests_data.infos

    def get_doc_id(self, url):
        for result in self.gen_get_doc_id():
            return result

    def gen_get_doc_id(self):
        for k in range(10):
            yield k

    def suggestions(self):
        for link in self.gen_suggestions():
            return link

    def gen_suggestions(self):
        for link in suggestions:
            yield link


class TestFTPSwiftea(FTPSwiftea):
    def __init__(self, host, user, password):
        FTPSwiftea.__init__(self, host, user, password)

    def get_inverted_index(self):
        return {}, False

    def send_inverted_index(self, inverted_index):
        assert inverted_index == tests_data.inverted_index

    def compare_indexs(self):
        for result in self.gen_compare_index():
            return result

    def gen_compare_index(self):
        yield True
        yield False


class TestWebConnexion(WebConnexion):
    def __init__(self):
        WebConnexion.__init__(self)

    def get_code(self, url):
        return tests_data.code1, False, 1, url


class TestCrawler(Crawler):
    def __init__(self):
        self.site_informations = SiteInformations()
        if self.site_informations.STOPWORDS is None:
            speak('No stopwords, quit program')
            quit_program()
        self.file_manager = FileManager()
        self.ftp_manager = TestFTPSwiftea(tests_data.HOST_FTP, tests_data.USER, tests_data.PASSWORD)
        self.get_inverted_index()
        self.index_manager = InvertedIndex()
        self.index_manager.setInvertedIndex(self.inverted_index)
        self.index_manager.setStopwords(self.site_informations.STOPWORDS)
        self.database = TestDatabaseSwiftea(tests_data.HOST_DB, tests_data.USER, tests_data.PASSWORD, tests_data.NAME_DB)
        self.web_connexion = TestWebConnexion()

        self.infos = list()
        self.crawled_websites = 0

    def safe_quit(self):
        self.send_inverted_index()
        speak('Programm will quit')
        speak('end\n', 0)
        tests_data.reset()


class TestGlobal(object):
    def test_crawler(self):
        create_dirs()
        create_doc()
        try:
            mkdir(data.DIR_LINKS)
        except FileExistsError:
            pass
        def_links()
        crawler = TestCrawler()

        config = ConfigParser()
        config['DEFAULT'] = {
            'run': 'false',
            'reading_file_number': '0',
            'writing_file_number': '1',
            'reading_line_number': '0',
            'max_links': data.MAX_LINKS
        }
        with open(data.FILE_CONFIG, 'w') as configfile:
            config.write(configfile)

        crawler.start()

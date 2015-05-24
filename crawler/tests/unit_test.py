#!/usr/bin/python3

import requests as req
from reppy.cache import RobotsCache
from reppy.exceptions import ServerError
from os import mkdir, rmdir
from configparser import ConfigParser

import main
import stats
import package.module as module
from package.module import *
import package.data as data
from package.data import *
from package.parsers import Parser_encoding, MyParser
from package.web_connexion import WebConnexion
from package.file_manager import FileManager
from package.database_swiftea import DatabaseSwiftea
import tests.test_data as test_data

class TestCrawlerBase(object):
    """Base class for all crawler test classes."""
    def setup_method(self, _):
        """Configure the app."""
        self.url = 'http://www.example.en'
        self.STOPWORDS = {'fr':('mot', 'pour')}
        self.inverted_index = {'EN': {
        'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}},
        'W': {'wo': {'word': {1: .3, 30: .4}}}}, 'FR': {
        'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}}}}
        self.max_links = 3
        self.writing_file_number = 5
        self.reading_file_number = 1
        self.reading_line_number = 0
        self.parser = MyParser()
        self.parser_encoding = Parser_encoding()
        self.objet = 'title'
        self.title = 'letter'
        self.code1 = test_data.code1
        self.code2 = test_data.code2
        self.code3 = test_data.code3
        self.reqrobots = RobotsCache()
        self.headers = {'status': '200 OK', 'content-type': 'text/html; charset=utf-8', 'vary': 'X-PJAX, Accept-Encoding'}
        self.config = ConfigParser()
        self.run = 'true'
        self.links = ['http://www.example.en/page.php', 'http://www.example.fr',
            'http://www.example.fr?w=word', 'http://www.example.en/page1']


class TestCrawlerFunctions(TestCrawlerBase):
    def test_average(self):
        assert average(['20', '20', '30', '30']) == 25

    def test_create_dirs(self):
        create_dirs()

    def test_create_doc(self):
        create_doc()
        create_doc()
        with open(FILE_DOC, 'w') as myfile:
            myfile.write('This is not the doc.')
        create_doc()

    def test_speak(self):
        tell('A test message', 0)
        tell('Beg test', severity=2)

    def test_get_stopwords(self):
        get_stopwords()
        get_stopwords(self.url)

    def test_is_index(self):
        assert is_index() == False
        open(FILE_INDEX, 'w').close()
        assert is_index() == True

    def test_stats(self):
        stats_links(30)
        stats_stop_words(100, 10)
        stats_stop_words(0, 0)
        stats_webpages(10, 30)
        stats_dl_index(10, 30)
        stats_ul_index(10, 30)

    def test_url_is_secure(self):
        assert url_is_secure(self.url) == False
        assert url_is_secure('https://www.example.en') == True

    def test_convert_secure(self):
        assert convert_secure(self.url) == 'https://www.example.en'
        assert convert_secure('https://www.example.en') == self.url


class TestWebConnexion(TestCrawlerBase):
    def test_is_nofollow(self):
        nofollow, url = is_nofollow(self.url + '!nofollow!')
        assert nofollow == True
        assert url == self.url
        nofollow, url = is_nofollow(self.url)
        assert nofollow == False
        assert url == self.url

    def test_no_connexion(self):
        assert no_connexion(self.url) == True
        assert no_connexion() == False

    def test_all_urls(self):
        request = req.get("https://fr.wikipedia.org")
        assert all_urls(request, request.url) == ["https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal", "https://fr.wikipedia.org"]
        request = req.get("http://www.wordreference.com/")
        assert all_urls(request, request.url) == ["http://www.wordreference.com"]


    def test_search_encoding(self):
        assert  WebConnexion.search_encoding(self, {}, self.code3) == ('utf-8', 0)
        assert WebConnexion.search_encoding(self, self.headers, self.code3) == ('utf-8', 1)
        assert WebConnexion.search_encoding(self, {}, self.code1) == ('utf-8', 1)
        assert WebConnexion.search_encoding(self, {}, self.code2) == ('UTF-16 LE', 1)

    def test_check_robots_perm(self):
        assert WebConnexion.check_robots_perm(self, 'https://zestedesavoir.com') == True
        assert WebConnexion.check_robots_perm(self, 'https://www.facebook.com') == False
        assert WebConnexion.check_robots_perm(self, self.url) == True
        assert WebConnexion.check_robots_perm(self, 'http://wiki.bilboplanet.com') == True
        assert WebConnexion.check_robots_perm(self, 'http://premium.lefigaro.fr') == True


class TestParser(TestCrawlerBase):
    def test_can_append(self):
        assert can_append('about/ninf.php', 'noindex, nofollow') == None
        assert can_append('about/ninf.php', 'nofollow') == 'about/ninf.php!nofollow!'
        assert can_append('about/ninf.php', '') == 'about/ninf.php'
        assert can_append(None, '') is None

    def test_meta(self):
        language, description, objet = meta([('name', 'description'), ('content', 'Communauté du Libre partage')])
        assert description == 'Communauté du Libre partage'
        assert objet == 'description'

        language, description, objet = meta([('name', 'language'), ('content', 'fr')])
        assert language == 'fr'

        language, description, objet = meta([('http-equiv', 'content-language'), ('content', 'en')])
        assert language == 'en'


    def test_handle_entityref(self):
        MyParser.handle_entityref(self, 'eacute')
        assert self.title == 'letteré'
        MyParser.handle_entityref(self, 'agrave')
        assert self.title == 'letteréà'

    def test_handle_charref(self):
        pass


    def test_parser(self):
        parser = MyParser()
        parser.feed(self.code1)
        assert parser.links == ['demo', 'index', 'about/nf.php!nofollow!']
        assert clean_text(parser.first_title) == 'Gros titre'
        assert clean_text(parser.keywords) == 'Gros titre Moyen titre petit titre strong em'
        assert parser.css == True
        assert parser.description == 'Moteur de recherche'
        assert parser.language == 'en'
        assert parser.favicon == 'public/favicon.ico'
        assert parser.title == 'Swiftea'

        parser.feed(self.code2)
        assert parser.language == 'en'
        assert parser.favicon == 'public/favicon2.ico'

        parser.feed(self.code3)
        assert parser.language == 'fr'

    def test_parser_encoding(self):
        parser = Parser_encoding()
        parser.feed(self.code1)
        assert parser.encoding == 'utf-8'
        parser.feed(self.code2)
        assert parser.encoding == 'UTF-16 LE'


class TestFileManager(TestCrawlerBase):
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

    def test_ckeck_size_links(self):
        self.max_links = 2
        FileManager.ckeck_size_links(self, self.links)

    def test_get_url(self):
        mkdir(DIR_LINKS)
        with open(DIR_LINKS + '1', 'w') as myfile:
            myfile.write(self.url + '\nhttp://example.en/page qui parle de ça')
        assert FileManager.get_url(self) == self.url
        assert FileManager.get_url(self) == 'http://example.en/page qui parle de ça'
        self.reading_file_number = 1
        assert FileManager.get_url(self) == 'stop'

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


class TestReset(object):
    def test_reset(self):
        test_data.reset()

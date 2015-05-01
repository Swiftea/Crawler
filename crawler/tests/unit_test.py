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
from package.searches import SiteInformations
from package.inverted_index import InvertedIndex
from package.parsers import Parser_encoding, MyParser
from package.web_connexion import WebConnexion
from package.file_manager import FileManager
from package.database_swiftea import DatabaseSwiftea
import tests.tests_data as tests_data

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
        self.code1 = tests_data.code1
        self.code2 = tests_data.code2
        self.code3 = tests_data.code3
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

    def test_get_stopwords(self):
        get_stopwords()
        get_stopwords(self.url)

    def test_is_index(self):
        assert is_index() == False
        open(FILE_INDEX, 'w').close()
        assert is_index() == True

    def test_stats(self):
        stats_links(30)
        stats_stop_words(40, 20)
        stats_stop_words(20, 0)

    def test_url_is_secure(self):
        assert url_is_secure(self.url) == False
        assert url_is_secure('https://www.example.en') == True

    def test_convert_secure(self):
        assert convert_secure(self.url) == 'https://www.example.en'
        assert convert_secure('https://www.example.en') == self.url


class TestSearches(TestCrawlerBase):
    def test_get_base_url(self):
        assert get_base_url(self.url + '/page1.php') == self.url

    def test_clean_text(self):
        text = clean_text('Sample text with non-desired \r whitespaces \t chars \n')
        assert '\n' not in text and '\r' not in text and '\t' not in text

    def test_split_keywords(self):
        is_list, keywords = split_keywords('jean/pierre')
        assert is_list == True
        assert keywords == ['jean', 'pierre']
        is_list, keywords = split_keywords('fichier.ext')
        assert keywords == ['fichier', 'ext']
        is_list, keywords = split_keywords('fichier')
        assert is_list == False
        assert keywords == 'fichier'

    def test_letter_repeat(self):
        assert letter_repeat('file') == False
        assert letter_repeat('*****') == True
        assert letter_repeat('aaaaa') == True

    def test_is_letters(self):
        assert is_letters('file') == True
        assert is_letters('fi*le') == True
        assert is_letters('****') == False
        assert is_letters('2015') == False

    def test_check_size_keyword(self):
        assert check_size_keyword('keyword') == True
        assert check_size_keyword('in') == False
        assert check_size_keyword('the') == True

    def test_remove_duplicates(self):
        assert remove_duplicates(['word', 'word']) == ['word']

    def test_is_homepage(self):
        assert is_homepage('http://www.bfmtv.com') == True
        assert is_homepage('http://www.bfmtv.com/page.html') == False
        assert is_homepage('https://github.com') == True
        assert is_homepage('http://bfmbusiness.bfmtv.com') == False


    def test_remove_useless_chars(self):
        assert remove_useless_chars('(file’s)...') == 'file'
        assert remove_useless_chars('2.0') == '2.0'
        assert remove_useless_chars("fi'") is None
        assert remove_useless_chars("fi's") is None

    def test_clean_link(self):
        assert clean_link('http://www.example.fr?w=word#big_title') == 'http://www.example.fr?w=word'


    def test_clean_links(self):
        links = ['page.php', 'http://www.example.fr/', 'mailto:test@test.fr',
            '//www.example.fr?w=word', 'http://www.example.en/page1/index.html',
            '/page1', 'http:/', 'https://a.net', '://www.sportetstyle.fr']
        links = SiteInformations.clean_links(self, links, self.url)
        assert links == ['http://www.example.en/page.php', 'http://www.example.fr',
            'http://www.example.fr?w=word', 'http://www.example.en/page1', 'https://a.net', 'http://www.sportetstyle.fr']

    def test_clean_keywords(self):
        # 'jean/pierre', 'fichier.ext'
        keywords = ['le', 'mot', '2015', 'bureau', 'word\'s', 'l\'example', 'l’oiseau',
        'quoi...', '*****', 'epee,...', '2.0', 'fi\'s']
        keywords = SiteInformations.clean_keywords(self, keywords, 'fr')
        assert keywords == ['bureau', 'word', 'example', 'oiseau', 'quoi', 'epee']

    def test_detect_language(self):
        keywords = "un texte d'exemple pour tester la fonction".split()
        assert SiteInformations.detect_language(self, keywords, self.url) == 'fr'
        keywords = "un texte d'exemple sans stopwords".split()
        assert SiteInformations.detect_language(self, keywords, self.url) == ''

    def test_clean_favicon(self):
        assert SiteInformations.clean_favicon(self, '/icon.ico', self.url) == 'http://www.example.en/icon.ico'
        assert SiteInformations.clean_favicon(self, '//example.fr/icon.ico', self.url) == 'http://example.fr/icon.ico'
        assert SiteInformations.clean_favicon(self, 'icon.ico', self.url) == 'http://www.example.en/icon.ico'


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

    def test_param_duplicate(self):
        assert WebConnexion.param_duplicate(self, req.get('http://www.01net.com')) == 'http://www.01net.com'
        assert WebConnexion.param_duplicate(self, req.get('http://www.01net.com/?page=12')) == 'http://www.01net.com'
        assert WebConnexion.param_duplicate(self, req.get('https://www.google.fr/webhp?tab=Xw')) == 'https://www.google.fr/webhp?tab=Xw'


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


class TestIndex(TestCrawlerBase):
    def test_getInvertedIndex(self):
        assert InvertedIndex.getInvertedIndex(self) == {'EN': {
        'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}},
        'W': {'wo': {'word': {1: .3, 30: .4}}}}, 'FR': {
        'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}}}}

    def test_setInvertedIndex(self):
        InvertedIndex.setInvertedIndex(self, self.inverted_index)
        assert InvertedIndex.getInvertedIndex(self) == self.inverted_index

    def test_setStopwords(self):
        InvertedIndex.setStopwords(self, {'fr':('mot', 'pour', 'autre')})
        assert self.STOPWORDS == {'fr':('mot', 'pour', 'autre')}

    def test_add_word(self):
        # Add language:
        word_infos = {'word': 'fiesta', 'language': 'ES', 'first_letter': 'F', 'filename': 'fi', 'occurence': 6}
        InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)
        # Add letter:
        word_infos = {'word': 'avion', 'language': 'FR', 'first_letter': 'A', 'filename': 'av', 'occurence': 6}
        InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)
        # Add letter:
        word_infos = {'word': 'voler', 'language': 'FR', 'first_letter': 'V', 'filename': 'vo', 'occurence': 7}
        InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)
        # Add filename:
        word_infos = {'word': 'aboutir', 'language': 'FR', 'first_letter': 'A', 'filename': 'ab', 'occurence': 7}
        InvertedIndex.add_word(self, word_infos, doc_id=56, nb_words=40)
        # add word:
        word_infos = {'word': 'aviation', 'language': 'FR', 'first_letter': 'A', 'filename': 'av', 'occurence': 7}
        InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)
        # add doc_id:
        word_infos = {'word': 'aviation', 'language': 'FR', 'first_letter': 'A', 'filename': 'av', 'occurence': 4}
        InvertedIndex.add_word(self, word_infos, doc_id=10, nb_words=30)
        # add sp first letter:
        word_infos = {'word': 'ùaviation', 'language': 'FR', 'first_letter': 'SP', 'filename': 'sp-a', 'occurence': 7}
        InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)
        # add sp filename:
        word_infos = {'word': 'aùviation', 'language': 'FR', 'first_letter': 'A', 'filename': 'a-sp', 'occurence': 7}
        InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)
        # Update:
        word_infos = {'word': 'avion', 'language': 'FR', 'first_letter': 'A', 'filename': 'av', 'occurence': 7}
        InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)

        assert self.inverted_index == {'EN': {
        'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}},
        'W': {'wo': {'word': {1: .3, 30: .4}}}}, 'FR': {
        'V': {'vo': {'voler': {9: 7/40}}},
        'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}},
        'A': {'av': {'avion': {9: 7/40}, 'aviation': {9: 7/40, 10: 0.1333333}}, 'ab': {'aboutir': {56: 7/40}}, 'a-sp': {'aùviation': {9: 7/40}}},
        'SP': {'sp-a': {'ùaviation': {9: 7/40}}}}, 'ES': {'F': {'fi': {'fiesta': {9: 6/40}}}}}

    def test_delete_word(self):
        InvertedIndex.delete_word(self, 'above', 'EN', 'A', 'ab')
        assert self.inverted_index == {'EN': {
        'A': {'ab': {'abort': {1: .3, 2: .1}}},
        'W': {'wo': {'word': {1: .3, 30: .4}}}}, 'FR': {
        'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}}}}

    def test_delete_id_word(self):
        word_infos = {'word': 'boule', 'language': 'FR', 'first_letter': 'B', 'filename': 'bo'}
        InvertedIndex.delete_id_word(self, word_infos, 2)
        assert self.inverted_index == {'EN': {
        'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}},
        'W': {'wo': {'word': {1: .3, 30: .4}}}}, 'FR': {
        'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25}}}}}

    def test_delete_doc_id(self):
        InvertedIndex.delete_doc_id(self, 2)
        assert self.inverted_index == {'EN': {
        'A': {'ab': {'above': {1: .3}, 'abort': {1: .3}}},
        'W': {'wo': {'word': {1: .3, 30: .4}}}}, 'FR': {
        'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25}}}}}
        InvertedIndex.delete_doc_id(self, 1)
        print(self.inverted_index)
        assert self.inverted_index == {'EN': {'W': {'wo': {'word': {30: .4}}}}}


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
        tests_data.reset()

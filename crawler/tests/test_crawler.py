#!/usr/bin/python3

import requests
from reppy.cache import RobotsCache
from reppy.exceptions import ServerError


import package.module as module
from package.data import *
from package.searches import SiteInformations
from package.inverted_index import InvertedIndex
from package.parsers import Parser_encoding, MyParser
from package.web_connexion import WebConnexion
from package.file_manager import FileManager

class TestCrawlerBase(object):
    """Base class for all crawler test classes"""
    def setup_method(self, _):
        """Configure the app."""
        self.url = 'http://www.example.fr'
        self.language = 'fr'
        self.STOPWORDS = {'fr':('mot', 'pour')}
        self.inverted_index = {'EN': {
        'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}},
        'W': {'wo': {'word': {1: .3, 30: .4}}}}, 'FR': {
        'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}}}}

        self.max_links = 3
        self.writing_file_number = 5
        self.reading_file_number = 0
        self.reading_line_number = 1
        self.parser = MyParser()
        self.parser_encoding = Parser_encoding()
        self.code1 = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="Description" content="Moteur de recherche">
        <title>Swiftea</title>
        <link rel="stylesheet" href="public/css/reset.css">
        <link rel="icon" href="public/favicon.ico" type="image/x-icon">
    </head>
    <body>
        <a href="demo">CSS Demo</a>
        <h1>Gros titre</h1>
        <h2>Moyen titre</h2>
        <h3>petit titre</h3>
        <p><strong>strong </strong><em>em</em></p>
        <a href="index">
            <img src="public/themes/default/img/logo.png" alt="Swiftea">
        </a>
        <a href="about/ninf.php" rel="noindex, nofollow">Why use Swiftea ?</a>
        <a href="about/ni.php" rel="noindex">Why use Swiftea ?</a>
        <a href="about/nf.php" rel="nofollow">Why use Swiftea ?</a>
        <img src="public/themes/default/img/github.png" alt="Github Swiftea">
        <img src="public/themes/default/img/twitter.png" alt="Twitter Swiftea">
    </body>
</html>"""

        self.code2 = """<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-language" content="en">
        <link rel="shortcut icon" href="public/favicon2.ico" type="image/x-icon">
    </head>
    <body>
    </body>
</html>"""

        self.code3 = """<!DOCTYPE html>
<html>
    <head>
        <meta name="language" content="fr">
    </head>
    <body>
    </body>
</html>"""

        self.reqrobots = RobotsCache()

class TestCrawlerBasic(TestCrawlerBase):
    def test_clean_text(self):
        text = module.clean_text('Sample text with non-desired \r whitespaces \t chars \n')
        assert not '\n' in text and not '\r' in text and not '\t' in text

    def test_get_base_url(self):
        assert module.get_base_url(self.url + '/page1.php') == self.url

    def test_clean_links(self):
        links = ['page.php', 'http://www.example.fr/', 'mailto:test@test.fr']
        links = SiteInformations.clean_links(self, links)

        assert links == ['http://www.example.fr/page.php', 'http://www.example.fr']

    def test_clean_keywords(self):
        keywords = ['le', 'mot', '2015', 'bureau', 'word\'s', 'l\'example', 'l’oiseau',
        'jean/pierre', 'quoi...', '*****', 'fichier.ext', 'epee,...']
        keywords = SiteInformations.clean_keywords(self, keywords)
        assert keywords == ['bureau', 'word', 'example', 'oiseau', 'jean', 'pierre', 'quoi', 'fichier', 'epee']

    def test_remove_duplicates(self):
        assert module.remove_duplicates(['mot', 'mot']) == ['mot']

    def test_detect_language(self):
        keywords = 'un texte d\'exemple pour tester la fonction'.split()
        language = SiteInformations.detect_language(self, keywords)
        assert language == 'fr'

    def test_clean_favicon(self):
        favicon = '/icon.ico'
        favicon = SiteInformations.clean_favicon(self, favicon)
        assert favicon == 'http://www.example.fr/icon.ico'

    def test_search_encoding(self):
        # don't test all ways
        url = 'https://github.com/topdelir1'
        request = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        encoding = WebConnexion.search_encoding(self, request)
        assert encoding[0] == 'utf-8'

    def test_check_robots_perm(self):
        perm = WebConnexion.check_robots_perm(self, 'https://zestedesavoir.com')
        assert perm == True
        perm = WebConnexion.check_robots_perm(self, 'https://www.facebook.com')
        assert perm == False

    def test_is_nofollow(self):
        nofollow, url = WebConnexion.is_nofollow(self, self.url + '!nofollow!')
        assert nofollow == True
        assert url == self.url
        nofollow, url = WebConnexion.is_nofollow(self, self.url)
        assert nofollow == False
        assert url == self.url

    def test_parser(self):
        parser = MyParser()
        parser.feed(self.code1)
        assert parser.links == ['demo', 'index', 'about/nf.php!nofollow!']
        assert module.clean_text(parser.first_title) == 'Gros titre'
        assert module.clean_text(parser.keywords) == "Gros titre Moyen titre petit titre strong em"
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

    def test_average(self):
        assert module.average(['20', '20', '30', '30']) == 25

    def test_getInvertedIndex(self):
        assert InvertedIndex.getInvertedIndex(self) == {'EN': {
        'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}},
        'W': {'wo': {'word': {1: .3, 30: .4}}}}, 'FR': {
        'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}}}}

    def test_add_word(self):
        # add language:
        word_infos = {'word': 'avion', 'language': 'FR', 'first_letter': 'A', 'filename': 'av', 'occurence': 6}
        InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)
        # add letter:
        word_infos = {'word': 'voler', 'language': 'FR', 'first_letter': 'V', 'filename': 'vo', 'occurence': 7}
        InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)
        # add filename:
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
        # update:
        word_infos = {'word': 'avion', 'language': 'FR', 'first_letter': 'A', 'filename': 'av', 'occurence': 7}
        InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)

        assert self.inverted_index == {'EN': {
        'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}},
        'W': {'wo': {'word': {1: .3, 30: .4}}}}, 'FR': {
        'V': {'vo': {'voler': {9: 7/40}}},
        'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}},
        'A': {'av': {'avion': {9: 7/40}, 'aviation': {9: 7/40, 10: 0.1333333}}, 'ab': {'aboutir': {56: 7/40}}, 'a-sp': {'aùviation': {9: 7/40}}},
        'SP': {'sp-a': {'ùaviation': {9: 7/40}}}}}

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

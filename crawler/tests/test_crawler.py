#!/usr/bin/python3

import requests


from package.module import *
from package.data import *
from package.searches import SiteInformations
from package.inverted_index import InvertedIndex
from package.parsers import Parser_encoding, MyParser
from package.web_connexion import WebConnexion
from statistiques import average

class TestCrawlerBase(object):
    """Base class for all crawler test classes"""
    def setup_method(self, _):
        """Configure the app."""
        self.url = 'http://www.example.fr'
        self.language = 'fr'
        self.STOPWORDS = {'fr':('mot', 'pour')}
        self.inverted_index = {'EN': {'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}, 'wo': {'word': {1: .3, 30: .4}}}, 'B': {}},
        'FR': {'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}}}}
        self.alphabet = ALPHABET
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

class TestCrawlerBasic(TestCrawlerBase):
    def test_clean_text(self):
        text = clean_text('Sample text with non-desired \r whitespaces \t chars \n')
        assert not '\n' in text and not '\r' in text and not '\t' in text

    def test_get_base_url(self):
        assert get_base_url(self.url + '/page1.php') == self.url

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
        assert remove_duplicates(['mot', 'mot']) == ['mot']

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

    def test_parser(self):
        parser = MyParser()
        parser.feed(self.code1)
        assert parser.links == ['demo', 'index', 'about/nf.php!nofollow!']
        assert clean_text(parser.first_title) == 'Gros titre'
        assert clean_text(parser.keywords) == "Gros titre Moyen titre petit titre strong em"
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

    def test_stats_links(self):
        assert average(['20', '20', '30', '30']) == 25

    def test_getInvertedIndex(self):
        assert InvertedIndex.getInvertedIndex(self) == {'EN': {'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}, 'wo': {'word': {1: .3, 30: .4}}}, 'B': {}},
        'FR': {'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}}}}

    def test_add_word(self):
        InvertedIndex.add_word(self, 'avion', 'FR', 'A', 'av', occurence=6, doc_id=9, nb_words=40)
        #print(self.inverted_index)
        assert self.inverted_index['FR']['A']['av']['avion'][9] == 6 / 40
        #assert self.inverted_index['FR']['A']['av'] == {'avion': {9 :6 / 40}}
        #assert self.inverted_index['FR']['A'] == {'av': {'avion': {9 :6 / 40}}}
        #assert self.inverted_index == {'EN': {'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}, 'wo': {'word': {1: .3, 30: .4}}}, 'B': {}},
        #'FR': {'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}}, 'A': {'av': {'avion': {9: .15}}}}}

    def test_add_doc(self):
        pass
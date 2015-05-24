#!/usr/bin/python3

from package.module import *
from package.searches import SiteInformations
from tests.unit_test import TestCrawlerBase

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

    def test_remove_duplicates(self):
        assert remove_duplicates(['word', 'word']) == ['word']

    def test_is_homepage(self):
        assert is_homepage('http://www.bfmtv.com') == True
        assert is_homepage('http://www.bfmtv.com/page.html') == False
        assert is_homepage('https://github.com') == True
        assert is_homepage('http://bfmbusiness.bfmtv.com') == False

    def test_capitalize(self):
        assert capitalize('ceci est un Titre') == 'Ceci est un Titre'
        assert capitalize('') == ''

    def test_remove_useless_chars(self):
        assert remove_useless_chars('(file’s)...') == 'file'
        assert remove_useless_chars('2.0') == '2.0'

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
        'quoi...', '*****', 'epee,...', '2.0', 'o\'clock']
        keywords = SiteInformations.clean_keywords(self, keywords, 'fr')
        assert keywords == ['le', 'bureau', 'word', 'example', 'oiseau', 'quoi', 'epee', 'clock']

    def test_detect_language(self):
        keywords = "un texte d'exemple pour tester la fonction".split()
        assert SiteInformations.detect_language(self, keywords, self.url) == 'fr'
        keywords = "un texte d'exemple sans stopwords".split()
        assert SiteInformations.detect_language(self, keywords, self.url) == ''

    def test_clean_favicon(self):
        assert SiteInformations.clean_favicon(self, '/icon.ico', self.url) == 'http://www.example.en/icon.ico'
        assert SiteInformations.clean_favicon(self, '//example.fr/icon.ico', self.url) == 'http://example.fr/icon.ico'
        assert SiteInformations.clean_favicon(self, 'icon.ico', self.url) == 'http://www.example.en/icon.ico'

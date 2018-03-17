#!/usr/bin/python3

from main import crawl, clean_text
from objects.webpage import Webpage

class TestMain():
    def test_crawl(self):
        assert type(crawl('https://huluti.github.io')) == Webpage

    def test_clean_text(self):
        assert clean_text(' test ') == 'test'

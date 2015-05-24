#!/usr/bin/python3

from package.module import *
from package.inverted_index import InvertedIndex
from tests.unit_test import TestCrawlerBase

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

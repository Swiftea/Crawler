#!/usr/bin/env python3

from index.index import stats_dl_index, stats_ul_index, count_files_index
from index.inverted_index import InvertedIndex
from tests.test_data import INVERTED_INDEX


class IndexBaseTest(object):
	def setup_method(self, _):
		self.inverted_index = {'EN': {
		'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}},
		'W': {'wo': {'word': {1: .3, 30: .4}}}}, 'FR': {
		'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}}}}


class TestIndex(IndexBaseTest):
	def test_stats_dl_index(self):
		stats_dl_index(100, 130)

	def test_stats_ul_index(self):
		stats_ul_index(100, 130)

	def test_count_files_index(self):
		assert count_files_index(self.inverted_index) == 4


class TestInvertedIndex(IndexBaseTest):
	def test_create_inverted_index(self):
		inverted_index = InvertedIndex()

	def test_getInvertedIndex(self):
		assert InvertedIndex.getInvertedIndex(self) == INVERTED_INDEX

	def test_setInvertedIndex(self):
		InvertedIndex.setInvertedIndex(self, self.inverted_index)
		assert InvertedIndex.getInvertedIndex(self) == self.inverted_index
		InvertedIndex.setInvertedIndex(self, '')
		assert InvertedIndex.getInvertedIndex(self) == dict()

	def test_add_doc(self):
		index = InvertedIndex()
		index.setInvertedIndex(self.inverted_index)
		keywords = ['le', '2015', 'bureau', 'word', 'example', 'oiseau', 'quoi', 'epee', 'clock', 'çochon', '12h', 'a3']
		index.add_doc(keywords, 13, 'fr')
		assert index.inverted_index == {'EN': {'A': {'ab': {'above': {1: 0.3, 2: 0.1}, 'abort': {1: 0.3, 2: 0.1}}}, 'W': {'wo': {'word': {1: 0.3, 30: 0.4}}}}, 'FR': {'B': {'ba': {'bateau': {1: 0.5}}, 'bo': {'boule': {1: 0.25, 2: 0.8}}, 'bu': {'bureau': {13: 0.0833333}}}, 'L': {'le': {'le': {13: 0.0833333}}}, 'SP': {'sp-sp': {'2015': {13: 0.0833333}, '12h': {13: 0.0833333}}, 'sp-o': {'çochon': {13: 0.0833333}}}, 'W': {'wo': {'word': {13: 0.0833333}}}, 'E': {'ex': {'example': {13: 0.0833333}}, 'ep': {'epee': {13: 0.0833333}}}, 'O': {'oi': {'oiseau': {13: 0.0833333}}}, 'Q': {'qu': {'quoi': {13: 0.0833333}}}, 'C': {'cl': {'clock': {13: 0.0833333}}}, 'A': {'a-sp': {'a3': {13: 0.0833333}}}}}


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
		# Add word:
		word_infos = {'word': 'aviation', 'language': 'FR', 'first_letter': 'A', 'filename': 'av', 'occurence': 7}
		InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)
		# Add doc_id:
		word_infos = {'word': 'aviation', 'language': 'FR', 'first_letter': 'A', 'filename': 'av', 'occurence': 4}
		InvertedIndex.add_word(self, word_infos, doc_id=10, nb_words=30)
		# Add sp first letter:
		word_infos = {'word': 'ùaviation', 'language': 'FR', 'first_letter': 'SP', 'filename': 'sp-a', 'occurence': 7}
		InvertedIndex.add_word(self, word_infos, doc_id=9, nb_words=40)
		# Add sp filename:
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
		assert self.inverted_index == {'EN': {'W': {'wo': {'word': {30: .4}}}}}

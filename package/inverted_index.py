#!/usr/bin/python3

"""Class for manage the inverted index."""

__author__ = "Seva Nathan"

from time import time


from package.module import speak
from package.data import TIMEOUT_INDEX

class InvertedIndex:
	"""Manage the inverted index for the crawler."""
	def __init__(self):
		"""Build the InvertedIndex manager.

		example : 
		'word'{1:12,20:39}'site'{2:14}
		the word 'word' is 20 times in the first document,
		the word 'site' is 14 times in the document 2.

		"""
		self.index = str()
		self.STOP_WORDS = dict()

	def setSTOP_WORDS(self, STOP_WORDS):
		"""Define STOP_WORDS."""
		self.STOP_WORDS = STOP_WORDS

	def setIndex(self, index):
		"""Define the index at the beginning."""
		self.index = index

	def getIndex(self):
		"""Retrun the index."""
		return self.index

	def append_doc(self, infoswebpage, id0):
		"""Add all words of a doc in the index."""
		words_add = infoswebpage['keywords']
		keywords_title = self.generate_keywords(infoswebpage['title'], infoswebpage['language'])
		words_add.extend(keywords_title)

		beginning = time()

		for word in words_add:
			now = time()
			if now - beginning < TIMEOUT_INDEX:
				occurence = words_add.count(word)
	
				place_word = self.index.find("'" + word + "'")
				if place_word != -1:
					# if the word is in the index
					place_end = self.index.find('}', place_word)
					if self.index.find(str(id0), place_word, place_end) == -1:
						place_apo = self.index.find('\'', place_end)
						self.index = self.index[:place_end] + ',' + str(id0) + ':' + str(occurence) + self.index[place_apo-1:]
				else:
					# if we need to add it in the index
					self.index += "'" + word + "'{" + str(id0) + ':' + \
						str(occurence) +  '}'
			else:
				# indexation too long : next doc
				speak('indexation trop longue : on passe.', 23)
				return 'del'

		words_add = list(set(words_add))
		self.save_keyword(words_add) # tests

		return 'ok'

	def generate_keywords(self, title, language):
		if language == 'fr':
			stop_words = self.STOP_WORDS['fr']
		elif language == 'en':
			stop_words = self.STOP_WORDS['en']
		elif language == 'es':
			stop_words = self.STOP_WORDS['es']
		elif language == 'it':
			stop_words = self.STOP_WORDS['it']
		else:
			stop_words = []
	
		title = title.lower().strip().split()
		result = []
	
		for key, value in enumerate(title):
			title[key] = value.strip()
	
		for value in title:
			if len(value) > 2:
				if value not in stop_words:
					result.append(value)
	
		return result

	# for testing : 

	def save_index(self, name='save_index.txt'):
		"""Save the index in a file to check errors."""
		with open(name, 'w', encoding='utf-8', errors='replace') as myfile:
			myfile.write(str(self.index))
			myfile.write('\n')

	def save_keyword(self, words_add):
		"""Save the keywords in a file to check errors."""
		with open('save_keywords.txt', 'a', encoding='utf-8', errors='replace') as myfile:
			myfile.write(str(words_add))
			myfile.write('\n\n')
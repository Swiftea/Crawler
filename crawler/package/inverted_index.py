#!/usr/bin/python3

"""Class for manage the inverted inverted_index."""

__author__ = "Seva Nathan"

from time import time


from package.module import speak
from package.data import INDEXING_TIMEOUT, DIR_OUTPUT

class InvertedIndex:
	"""Manage the inverted inverted_index for the crawler."""
	def __init__(self):
		"""Build the InvertedIndex manager.

		example :
		'word'{1:12,20:39}'site'{2:14}
		the word 'word' is 20 times in the first document,
		the word 'site' is 14 times in the document 2.

		"""
		self.inverted_index = str()
		self.STOPWORDS = dict()

	def setStopwords(self, STOPWORDS):
		"""Define STOPWORDS."""
		self.STOPWORDS = STOPWORDS

	def setInvertedIndex(self, inverted_index):
		"""Define inverted_index at the beginning."""
		self.inverted_index = inverted_index

	def getInvertedIndex(self):
		"""Return inverted inverted_index."""
		return self.inverted_index

	def append_doc(self, webpage_infos, doc_id):
		"""Add all words of a doc in the inverted_index."""
		words_to_add = webpage_infos['keywords']
		title_keywords = self.generate_keywords(webpage_infos['title'], webpage_infos['language'])
		words_to_add.extend(title_keywords)

		beginning = time()

		for word in words_to_add:
			now = time()
			if now - beginning < INDEXING_TIMEOUT:
				occurence = words_to_add.count(word)

				word_position = self.inverted_index.find("'" + word + "'")
				if word_position != -1:
					# if the word is in the inverted index :
					end_position = self.inverted_index.find('}', word_position)
					if self.inverted_index.find(doc_id, word_position, end_position) == -1:
						quote_position = self.inverted_index.find('\'', end_position)
						self.inverted_index = self.inverted_index[:end_position] + ',' + doc_id + ':' + str(occurence) + self.inverted_index[quote_position-1:]
				else:
					# if we need to add it in the inverted_index :
					self.inverted_index += "'" + word + "'{" + doc_id + ':' + str(occurence) +  '}'
			else:
				speak('Indexing too long : pass', 23)
				return True

		self.save_keyword(list(set(words_to_add))) # tests

		return False

	def generate_keywords(self, title, language):
		if language == 'fr':
			stopwords = self.STOPWORDS['fr']
		elif language == 'en':
			stopwords = self.STOPWORDS['en']
		elif language == 'es':
			stopwords = self.STOPWORDS['es']
		elif language == 'it':
			stopwords = self.STOPWORDS['it']
		else:
			stopwords = []

		title = title.lower().strip().split()
		result = []

		for key, value in enumerate(title):
			title[key] = value.strip()

		for value in title:
			if len(value) > 2:
				if value not in stopwords:
					result.append(value)

		return result

	# for testing :

	def save_index(self, name='save_index.txt'):
		"""Save the inverted_index in a file to check errors."""
		with open(DIR_OUTPUT + name, 'w', encoding='utf-8', errors='replace') as myfile:
			myfile.write(str(self.inverted_index))
			myfile.write('\n')

	def save_keyword(self, words_to_add):
		"""Save the keywords in a file to check errors."""
		with open(DIR_OUTPUT + 'save_keywords.txt', 'a', encoding='utf-8', errors='replace') as myfile:
			myfile.write(str(words_to_add))
			myfile.write('\n\n')

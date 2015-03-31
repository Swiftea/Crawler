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
		'word'1:12,20:39'site'2:14
		the word 'word' is 20 times in the first document,
		the word 'site' is 14 times in the document 2.

		self.inverted_index = {'a': "'avion1:2'", 'b': "'bateau'2:2"}

		"""
		self.inverted_index = dict()
		self.alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
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

	def append_doc(self, keywords, doc_id):
		"""Add all words of a doc in the inverted_index.

		Take a list of keywords  and return a list contain modify dicts.
		The list given must be contain page keywords and title keywords, and purhap description keywords.

		"""
		beginning = time()
		new_inverted_index = dict()
		for word in keywords:
			if time() - beginning < INDEXING_TIMEOUT:
				occurence = str(keywords.count(word))
				first_letter = word[0]
				if first_letter in self.alphabet:
					# it's a letter
					if first_letter in self.inverted_index.keys():
						# the key exists in th dict
						# take the value of the dict
						inverted_index = self.inverted_index[first_letter]
					else:
						# add the key and value in the dict
						self.inverted_index[first_letter] = inverted_index = str()
				else:
					# the first char isn't a letter
					if '_' in self.inverted_index.keys():
						inverted_index = self.inverted_index['_']
					else:
						self.inverted_index['_'] = inverted_index = str()
				word_position = inverted_index.find("'" + word + "'")
				if word_position != -1:
					# the word is in the inverted-index
					word_position += 1
					end_position = inverted_index.find("}", word_position)
					# add doc and occurence in inverted-index :
					doc_id_position = inverted_index.find(doc_id + ':', word_position, end_position)
					quote_position = inverted_index.find("'", end_position)
					if doc_id_position != -1:
						# there is already the doc to the word, update occurence :
						inverted_index = inverted_index[:doc_id_position+2] + occurence + inverted_index[doc_id_position + len(occurence) +2:]
					else:
						# there isn't the doc to this word :
						if quote_position != -1:
							inverted_index = inverted_index[:end_position] + ',' + doc_id + ':' + occurence + inverted_index[quote_position-1:]
						else:
							# if there is only one word :
							inverted_index = inverted_index[:end_position] + ',' + doc_id + ':' + occurence + '}'
				else:
					# adding the word in the inverted-index :
					inverted_index += "'" + word + "'{" + doc_id + ':' + occurence + '}'

				new_inverted_index[first_letter] = inverted_index
				self.inverted_index[first_letter] = inverted_index

			else:
				speak('Indexing too long : pass', 23)
				return None

		#self.save_keyword(str(list(set(words_to_add)))) # tests

		return new_inverted_index

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

		title = title.lower().split()

		for key, value in enumerate(title):
			title[key] = value.strip()

		result = []
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
			myfile.write(words_to_add)
			myfile.write('\n\n')
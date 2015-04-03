#!/usr/bin/python3

"""Class for manage the inverted inverted_index."""

__author__ = "Seva Nathan"

from time import time


from package.module import speak
from package.data import INDEXING_TIMEOUT, DIR_OUTPUT, ALPHABET

class InvertedIndex:
	"""Manage the inverted inverted_index for the crawler."""
	def __init__(self):
		"""Build the InvertedIndex manager.

		example :
		'word'{1:12,20:39}'site'{2:14}
		the word 'word' is 20 times in the first document,
		the word 'site' is 14 times in the document 2.

		"""
		self.inverted_index = dict()
		self.alphabet = ALPHABET
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
						first_letter = '_'
					else:
						self.inverted_index['_'] = inverted_index = str()
						first_letter = '_'
				word_pos = inverted_index.find("'" + word + "'")
				if word_pos != -1:
					# the word is in the inverted-index
					word_pos += 1
					end_pos = inverted_index.find("}", word_pos)
					# add doc and occurence in inverted-index :
					doc_id_pos = inverted_index.find(doc_id + ':', word_pos, end_pos)
					quote_pos = inverted_index.find("'", end_pos)
					coma_pos = inverted_index.find(",", doc_id_pos)
					two_pts_pos = len(doc_id) + doc_id_pos
					if doc_id_pos != -1:
						if coma_pos != -1:
						# there is already the doc to the word, update occurence :
							old_occ = inverted_index[two_pts_pos:coma_pos]
							inverted_index = inverted_index[:doc_id_pos] + inverted_index[doc_id_pos:].replace(old_occ, occurence, 0)
						else:
							# if it is the last doc : {1:1} -> {1:2}
							inverted_index = inverted_index[:doc_id_pos + len(doc_id) + 1] + occurence + inverted_index[two_pts_pos + len(occurence) +1:]
					else:
						# there isn't the doc to this word :
						if quote_pos != -1:
							inverted_index = inverted_index[:end_pos] + ',' + doc_id + ':' + occurence + inverted_index[quote_pos -1:]
						else:
							# if there is only one word :
							inverted_index = inverted_index[:end_pos] + ',' + doc_id + ':' + occurence + '}'
				else:
					# adding the word in the inverted-index :
					inverted_index += "'" + word + "'{" + doc_id + ':' + occurence + '}'

				new_inverted_index[first_letter] = inverted_index
				self.inverted_index[first_letter] = inverted_index

			else:
				speak('Indexing too long : pass', 23)
				return None

		#self.save_keyword(keywords) # tests

		return new_inverted_index

	# for testing :

	def save_index(self, name='save_index.txt'):
		"""Save the inverted_index in a file to check errors."""
		with open(DIR_OUTPUT + name, 'w', encoding='utf-8', errors='replace') as myfile:
			myfile.write(str(self.inverted_index))
			myfile.write('\n')

	def save_keyword(self, keywords):
		"""Save the keywords in a file to check errors."""
		with open(DIR_OUTPUT + 'save_keywords.txt', 'a', encoding='utf-8', errors='replace') as myfile:
			myfile.write(str(keywords) + '\n\n')
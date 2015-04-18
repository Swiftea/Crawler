#!/usr/bin/python3

"""Class for manage the inverted inverted_index."""

__author__ = "Seva Nathan"

from time import time


from package.module import speak
from package.data import INDEXING_TIMEOUT, DIR_OUTPUT, ALPHABET

class InvertedIndex:
	"""Manage inverted-index for crawler

inverted_index = {
	'EN': { # language folder
		'A': { # first letter folder
			'ab': { # two first letter (filename)
				'above': {1: .3, 2: .1},
				'abort': {1: .3, 2: .1}
			},
			'wo': {
				'word': {
					1:  # id
						.3, # idf
					30: 
						.4
				}
			}
		},
		'B':{}
	},
	'FR': {
		'B': {
			'ba': {
				'bateau': {
					1:
						.5
				}
			},
			'bo': {
				'boule': {
					1:
						.25,
					2:
						.8
				}
			}
		}
	}
}

Inverted-index is a dict, each keys are language
	-> values are a dict, each keys are first letter
	-> values are dict, each keys are two first letters
	-> values are dict, each keys are word 
	-> values are dict, each keys are id
	-> values are int : tf-idf

example: 
['FR']['A']['av']['avion'][21] is tf-idf of word 'avion' in doc 21, language is FR

"""

	def __init__(self):
		"""Build inverted-index manager"""
		self.inverted_index = dict()
		self.STOPWORDS = dict()

	def setStopwords(self, STOPWORDS):
		"""Define STOPWORDS"""
		self.STOPWORDS = STOPWORDS

	def setInvertedIndex(self, inverted_index):
		"""Define inverted_index at the beginning"""
		self.inverted_index = inverted_index

	def getInvertedIndex(self):
		"""Return inverted inverted_index"""
		return self.inverted_index

	def append_doc(self, keywords, doc_id, language):
		"""Add all words of a doc in inverted-index

		:param keywords: all word in doc_id
		:type keywords: list
		:param doc_id: id of the doc in database
		:type doc_id: int
		:param language: language of word
		:type language: str
		:return: 

		"""
		beginning = time()
		new_inverted_index = list()
		for word in keywords:
			if time() - beginning < INDEXING_TIMEOUT:
				occurence = keywords.count(word)
				if word[0] in ALPHABET:
					first_letter = word[0].upper()
					# first char is a letter
					if word[1] in ALPHABET:
						# second char is a letter
						filename = word[:2]
					else:
						# second char isn't a letter
						filename = first_letter.lower() + '-sp'
				else:
					# first char isn't a letter
					first_letter = 'SP'
					if word[1] in ALPHABET:
						# second char is a letter
						filename = 'sp-' + word[1]
					else:
						# second char isn't a letter
						filename = 'sp-sp'

				self.inverted_index[language][first_letter][filename] = self.add_word(word, language, first_letter.lower(), filename, occurence, doc_id)

			else:
				speak('Indexing too long : pass', 23)
				return None

		#self.save_keyword(keywords) # tests

		return new_inverted_index

	def get_index(self, language, first_letter, filename):
		"""Get inverted-index corresponding to params

		:param language: language of word
		:type language: str
		:param first_letter: first letter of word
		:type first_letter: str
		:param filename: two first letters of word
		:type filename: str
		:return: inverted-index

		"""
		folder_language = self.inverted_index[language]
		folder_letter = folder_language[first_letter]
		filename = folder_letter[filename]
		inverted_index = self.inverted_index[language][first_letter][filename]
		# if all is correct : filename = inverted_index
		return inverted_index

	def add_word(self, word, language, first_letter, filename, occurence, doc_id, nb_words):
		"""Add a word in inverted-index

		:param word: word to delete
		:type word: str
		:param language: language of word
		:type language: str
		:param first_letter: first letter of word
		:type first_letter: str
		:param filename: two first letters of word
		:type filename: str
		:param occurence: occurence of the word in webpage
		:type occurence: int
		:param doc_id: id of the doc in database
		:type doc_id: int
		:return: inverted-index

		"""
		inverted_index = self.get_index(word, language, first_letter, filename)
		tf = self.calculate_tf(occurence, nb_words)
		if word in inverted_index.keys():
			# word exists
			docs = inverted_index[word]
			update = False
			for key, doc in enumerate(docs):
				if doc_id in doc[0]:
					update = True
					break
			if update:
				# word already in doc_id: update tf
				docs[key] = [doc_id, tf]
				inverted_index[word] = docs
			else:
				docs.append([doc_id, tf])

			inverted_index[word] = docs

		else:
			# word doesn't exists
			inverted_index[word] = [doc_id, tf]
		return inverted_index
		# or: self.inverted_index[language][first_letter][filename] = inverted_index

	def delete_word(self, word, language, first_letter, filename):
		"""Delete a word in inverted-index

		:param word: word to delete
		:type word: str
		:param language: language of word
		:type language: str
		:param first_letter: first letter of word
		:type first_letter: str
		:param filename: two first letters of word
		:type filename: str

		"""
		inverted_index = self.get_index(word, language, first_letter, filename)
		del inverted_index[word]

	def delete_id_word(self, word, language, first_letter, filename, doc_id):
		"""Delete a id of a word in inverted-index

		:param word: word to delete
		:type word: str
		:param language: language of word
		:type language: str
		:param first_letter: first letter of word
		:type first_letter: str
		:param filename: two first letters of word
		:type filename: str
		:param doc_id: id of the doc in database
		:type doc_id: int

		"""
		inverted_index = self.get_index(word, language, first_letter, filename)
		docs = inverted_index[word] # list of list: [[doc_id, tf], [doc_id, tf]]
		for key, doc in enumerate(docs):
			if doc[0] == doc_id:
				del docs[key]

	def delete_doc_id(self, doc_id):
		"""Delete a id in inverted-index

		:param doc_id: id to delete
		:type doc_id: int

		"""
		for folder_language in self.inverted_index:
			folder_language_ = self.inverted_index[folder_language]
			# language
			for folder_letter in folder_language_:
				folder_letter_ = folder_language_[folder_letter]
				# letter
				for filename in folder_letter_:
					filename_ = folder_letter_[filename]
					# two first letters: filename
					for inverted_index in filename_:
						inverted_index_ = filename_[inverted_index]
						for word in inverted_index_:
							word_ = inverted_index_[word]
							# word: list of docs
							for docs in word_:
								docs = word_[docs]
								# docs: list of doc_id and tf
								for key, doc in enumerate(docs):
									if doc[0] == doc_id:
										del docs[key]
										self.inverted_index[folder_language][folder_letter][filename][inverted_index][word] = docs

	def calculate_tf(self, occurence, nb_words):
		"""Calculate tf with occurence and nb words

		:param occurence: occurence of the word in webpage
		:type occurence: int
		:param nb_words: number of words in the doc_id
		:type nb_words: int
		:return: tf

		"""
		tf = occurence / nb_words
		return tf

	# for testing :

	def save_index(self, name='save_index.txt'):
		"""Save the inverted-index in a file to check errors"""
		with open(DIR_OUTPUT + name, 'w', encoding='utf-8', errors='replace') as myfile:
			myfile.write(str(self.inverted_index))
			myfile.write('\n')

	def save_keyword(self, words):
		"""Save keywords in a file to check errors"""
		with open(DIR_OUTPUT + 'save_keywords.txt', 'a', encoding='utf-8', errors='replace') as myfile:
			myfile.write(str(keywords) + '\n\n')
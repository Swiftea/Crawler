#!/usr/bin/python3

__author__ = "Seva Nathan"

from time import time


from package.module import speak
from package.data import INDEXING_TIMEOUT, DIR_OUTPUT, ALPHABET

class InvertedIndex:
	"""Manage inverted-index for crawler

	Inverted-index is a dict, each keys are language
		-> values are a dict, each keys are first letter
		-> values are dict, each keys are two first letters
		-> values are dict, each keys are word
		-> values are dict, each keys are id
		-> values are int : tf

	example:
	['FR']['A']['av']['avion'][21] is tf of word 'avion' in doc 21, language is FR

	"""

	def __init__(self):
		"""Build inverted-index manager"""
		self.inverted_index = dict()
		self.STOPWORDS = dict()

	def setStopwords(self, STOPWORDS):
		"""Define STOPWORDS"""
		self.STOPWORDS = STOPWORDS

	def setInvertedIndex(self, inverted_index):
		"""Define inverted-indexs at the beginning"""
		self.inverted_index = inverted_index

	def getInvertedIndex(self):
		""":return: inverted-indexs"""
		return self.inverted_index

	def add_doc(self, keywords, doc_id, language):
		"""Add all words of a doc in inverted-indexs

		:param keywords: all word in doc_id
		:type keywords: list
		:param doc_id: id of the doc in database
		:type doc_id: int
		:param language: language of word
		:type language: str
		:return: true if time out

		"""
		language = language.upper()
		nb_words = len(keywords)
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

				self.add_word(word, language, first_letter, filename, occurence, doc_id, nb_words)

			else:
				speak('Indexing too long : pass', 23)
				return True

		#self.save_index() # tests

		return False

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
		:param nb_words: number of words in the doc_id
		:type nb_words: int

		"""
		if language in self.inverted_index:
			if first_letter in self.inverted_index[language]:
				if filename in self.inverted_index[language][first_letter]:
					inverted_index = self.inverted_index[language][first_letter][filename]
				else:
					self.inverted_index[language][first_letter][filename] = inverted_index = dict()
			else:
				inverted_index = dict()
				self.inverted_index[language][first_letter] = dict()
		else:
			inverted_index = dict()
			self.inverted_index[language] = dict()
			self.inverted_index[language][first_letter] = dict()
			self.inverted_index[language][first_letter][filename] = dict()

		tf = round(occurence / nb_words, 7)
		if word in inverted_index:
			inverted_index[word][doc_id] = tf
		else:
			inverted_index[word] = {doc_id: tf}

		self.inverted_index[language][first_letter][filename] = inverted_index

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
		if self.inverted_index[language][first_letter][filename].get(word) is not None:
			del self.inverted_index[language][first_letter][filename][word]

	def delete_id_word(self, word, language, first_letter, filename, doc_id):
		"""Delete a id of a word in inverted-index

		This method delete a word from a document.

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
		if self.inverted_index[language][first_letter][filename][word].get(doc_id) is not None:
			del self.inverted_index[language][first_letter][filename][word][doc_id]

	def delete_doc_id(self, doc_id):
		"""Delete a id in inverted-index

		Doesn't work

		:param doc_id: id to delete
		:type doc_id: int

		"""
		for language in self.inverted_index:
			for first_letter in self.inverted_index[language]:
				for filename in self.inverted_index[language][first_letter]:
					for word in self.inverted_index[language][first_letter][filename]:
						if self.inverted_index[language][first_letter][filename][word].get(doc_id) is not None:
							del self.inverted_index[language][first_letter][filename][word][doc_id]
						if self.inverted_index[language][first_letter][filename][word] == {}:
							del self.inverted_index[language][first_letter][filename][word]
							break
					if self.inverted_index[language][first_letter][filename] == {}:
						del self.inverted_index[language][first_letter][filename]
						break
				if self.inverted_index[language][first_letter] == {}:
					del self.inverted_index[language][first_letter]
					break
			if self.inverted_index[language] == {}:
				del self.inverted_index[language]
				break

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

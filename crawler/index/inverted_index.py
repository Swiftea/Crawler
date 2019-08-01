#!/usr/bin/env python3

"""Define the class the handle the inverted index."""

from crawler.swiftea_bot.data import ALPHABET


class InvertedIndex:
	r"""Manage inverted-index for crawler.

	Inverted-index is a dict, each keys are language\n
		-> values are a dict, each keys are first letter\n
		-> values are dict, each keys are two first letters\n
		-> values are dict, each keys are word\n
		-> values are dict, each keys are id\n
		-> values are int: tf\n

	example:
	['FR']['A']['av']['avion'][21] is tf of word 'avion' in doc 21 in french.

	"""
	def __init__(self):
		self.inverted_index = dict()

	def set_inverted_index(self, inverted_index):
		"""Define inverted-index at the beginning.

		:param inverted_index: inverted-index
		:type inverted_index: dict

		"""
		if isinstance(inverted_index, dict):
			self.inverted_index = inverted_index
		else:
			self.inverted_index = dict()

	def get_inverted_index(self):
		""":return: inverted-index"""
		return self.inverted_index

	def add_doc(self, keywords, doc_id, language):
		"""Add all words of a doc in inverted-index.

		:param keywords: all word in doc_id
		:type keywords: list
		:param doc_id: id of the doc in database
		:type doc_id: int
		:param language: language of word
		:type language: str

		"""
		language = language.upper()
		nb_words = len(keywords)
		for word in keywords:
			occurrence = word[1]
			word = word[0]
			word_infos = {
				'word': word,
				'language': language,
				'occurrence': occurrence
			}
			if word[0] in ALPHABET:
				word_infos['first_letter'] = word[0].upper()
				# First char is a letter
				if word[1] in ALPHABET:
					# Second char is a letter
					word_infos['filename'] = word[:2]
				else:
					# second char isn't a letter
					word_infos['filename'] = word_infos['first_letter'].lower() + '-sp'
			else:
				# First char isn't a letter
				word_infos['first_letter'] = 'SP'
				if word[1] in ALPHABET:
					# Second char is a letter
					word_infos['filename'] = 'sp-' + word[1]
				else:
					# Second char isn't a letter
					word_infos['filename'] = 'sp-sp'

			self.add_word(word_infos, doc_id, nb_words)

	def add_word(self, word_infos, doc_id, nb_words):
		"""Add a word in inverted-index.

		:param word_infos: word infos: word, language, occurrence,
			first letter and two first letters
		:type word_infos: dict
		:param doc_id: id of the doc in database
		:type doc_id: int
		:param nb_words: number of words in the doc_id
		:type nb_words: int

		"""
		word = word_infos['word']
		language = word_infos['language']
		first_letter = word_infos['first_letter']
		filename = word_infos['filename']
		if language in self.inverted_index:
			if first_letter in self.inverted_index[language]:
				if filename in self.inverted_index[language][first_letter]:
					inverted_index = self.inverted_index[language][first_letter][filename]
				else:
					inverted_index = dict()
					self.inverted_index[language][first_letter][filename] = dict()
			else:
				inverted_index = dict()
				self.inverted_index[language][first_letter] = dict()
		else:
			inverted_index = dict()
			self.inverted_index[language] = dict()
			self.inverted_index[language][first_letter] = dict()
			self.inverted_index[language][first_letter][filename] = dict()

		tf = round(word_infos['occurrence'] / nb_words, 7)
		if word in inverted_index:
			inverted_index[word][doc_id] = tf
		else:
			inverted_index[word] = {doc_id: tf}
			# ex: {'foo': {'14': 2.3125, '23': 1.003}, 'bar': {'44': 1.113, '213': 1.103}}

		self.inverted_index[language][first_letter][filename] = inverted_index

	def delete_word(self, word, language, first_letter, filename):
		"""Delete a word in inverted-index.

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

	def delete_id_word(self, word_infos, doc_id):
		"""Delete an id of a word in inverted-index.

		This method delete a word from a document.

		:param word_infos: word infos: word, language, first letter and two first letters
		:type word_infos: dict
		:param doc_id: id of the doc in database
		:type doc_id: int

		"""
		word, language, first_letter, filename = word_infos['word'], word_infos['language'], \
			word_infos['first_letter'], word_infos['filename']
		if self.inverted_index[language][first_letter][filename][word].get(doc_id) is not None:
			del self.inverted_index[language][first_letter][filename][word][doc_id]

	def delete_doc_id(self, doc_id, language='*'):
		"""Delete a id in inverted-index.

		:param doc_id: id to delete
		:type doc_id: int

		"""
		new_inverted_index = dict()
		for language in self.inverted_index:
			new_inverted_index[language] = dict()
			for first_letter in self.inverted_index[language]:
				new_inverted_index[language][first_letter] = dict()
				for filename in self.inverted_index[language][first_letter]:
					new_inverted_index[language][first_letter][filename] = dict()
					for word in self.inverted_index[language][first_letter][filename]:
						new_inverted_index[language][first_letter][filename][word] = dict()
						for doc in self.inverted_index[language][first_letter][filename][word]:
							if doc != doc_id:
								new_inverted_index[language][first_letter][filename][word][doc] = \
									self.inverted_index[language][first_letter][filename][word][doc]

						if new_inverted_index[language][first_letter][filename][word] == dict():
							del new_inverted_index[language][first_letter][filename][word]
					if new_inverted_index[language][first_letter][filename] == dict():
						del new_inverted_index[language][first_letter][filename]
				if new_inverted_index[language][first_letter] == dict():
					del new_inverted_index[language][first_letter]
			if new_inverted_index[language] == dict():
				del new_inverted_index[language]
		self.inverted_index = new_inverted_index

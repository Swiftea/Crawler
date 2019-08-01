#!/usr/bin/env python3

"""Define the class the handle the inverted index in nosql mongodb format."""

from crawler.index.database_ii import connect, add_doc, delete_doc


class InvertedIndex:
	def __init__(self, MONGODB_CON_STRING):
		connect(MONGODB_CON_STRING)

	def add_doc(self, keywords, doc_id, language):
		add_doc(keywords, doc_id, language)

	def delete_doc_id(self, doc_id, language='*'):
		delete_doc(doc_id, language)

import urllib.parse

import pymongo
from pymongo.write_concern import WriteConcern
from pymodm import connection, MongoModel, EmbeddedMongoModel, fields, errors

"""
Reference and MongoModel Document:
 - no possible because a document has multiple word

Embedded document model:
 - must iterate over document to add a new one
 - hard to delete a document

Embedded dict:
 - easy to add and update document
 - hard to delete a document

"""
from swiftea_bot.private_data import MONGODB_PASSWORD


class Document(EmbeddedMongoModel):
	id = fields.BigIntegerField(primary_key=True)
	tf = fields.FloatField()

	class Meta:
		write_concern = WriteConcern(j=True)
		connection_alias = 'my-app'
		final = True

class Word(MongoModel):
	word = fields.CharField()
	documents = fields.DictField(blank=True)
	language = fields.CharField()

	class Meta:
		write_concern = WriteConcern(j=True)
		connection_alias = 'my-app'
		final = True

def connect():
	password = urllib.parse.quote(MONGODB_PASSWORD)
	username = 'swiftea_admin'
	database_name = 'inverted_index'
	db_url = 'mongodb+srv://{}:{}@clusterswiftea-oz7b3.mongodb.net/{}?retryWrites=true&w=majority'.format(username, password, database_name)
	connection.connect(db_url, alias="my-app")

def add_word(word, doc_id, nb_words, language, occurrence):
	tf = round(occurrence / nb_words, 7)
	try:
		w = Word.objects.get({'word': word, 'language': language})
	except errors.DoesNotExist:
		w = Word(word, {doc_id: tf}, language).save()
	else:
		w.documents[doc_id] = tf
		w.save()

def add_doc(keywords, doc_id, language):
	nb_words = len(keywords)
	for word in keywords:
		add_word(word[0], doc_id, nb_words, language, word[1])

def delete_word(id):
	Word.objects.get({'_id': id}).delete()

def delete_doc(doc_id, language='*'):
	"""Use language to limit the raws to read."""
	if language == '*':
		words = Word.objects.all()
	else:
		words = Word.objects.raw({'language': language})
	for word in words:
		if doc_id in word.documents:
			if len(word.documents) == 1:
				delete_word(word._id)
			else:
				del word.documents[doc_id]
				word.save()

def test():
	"""Test functions"""
	add_word('camion', '5', 80, 'fr', 3)
	add_word('camion', '6', 30, 'fr', 1)
	add_word('mercato', '7', 30, 'it', 11)
	add_word('action', '36', 25, 'fr', 2)
	add_word('action', '37', 62, 'en', 3)

	add_doc(['buongiorno', 'capisco', 'chiamo', 'chiamo'], '7', 'it')

	# delete_doc('7', 'it')
	delete_doc('36', 'fr')
	delete_doc('5', 'en')

def experimentations():
	# create
	Word('répondre', {'1': 0.1418, '7': 0.0319}, 'fr').save()
	Word('delete', {'1': 0, '7': 0}, 'en').save()
	Word('but', {'1': 0, '7': 0}, 'en').save()
	Word('but', {'2': 0.185, '6': 0.13}, 'fr').save()
	# Word('action', {'2': 0.185, '6': 0.13}, 'fr').save()
	# Word('action', {'2': 0.185, '6': 0.13, '12': 0.185}, 'fr').save()
	# Word('action', {'25': 0.1841487}, 'fr').save()
	# Word('avion', {}, 'fr').save()  # {'documents': ['must not be blank (was: {})']}
	# Word('voiture', None, 'fr').save()  # {'documents': ['must not be blank (was: None)']}
	Word('voiture', language='fr').save()


	# get
	# w = Word.objects.get({'word': 'vélo'})  # __main__.DoesNotExist
	w = Word.objects.raw({'word': 'vélo'})
	# print(w)
	# print(w.values())
	# print(dir(w))
	# print(w.first())  # __main__.DoesNotExist

	# update: add doc
	w = Word.objects.get({'word': 'répondre'})
	w.documents['8'] = 0.00001
	w.save()

	# update: update doc
	w = Word.objects.get({'word': 'répondre'})
	w.documents['8'] = 0.00005
	w.save()

	# delete word
	w = Word.objects.get({'word': 'delete', 'language': 'en'}).delete()

	# delete doc
	doc_id = '7'
	for word in Word.objects.raw({'language': 'fr'}):
		if doc_id in word.documents:
			del word.documents[doc_id]
			word.save()

	# # TODO: index: language.word

if __name__ == '__main__':
	connect()
	# experimentations()
	test()

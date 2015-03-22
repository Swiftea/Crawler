#!/usr/bin/

"""Class to manage the ftp connexion for swiftea."""

from package.FTP import FTPConnect
from package.data import FILE_INDEX, FTP_INDEX
from package.module import speak

__author__ = "Seva Nathan"

class FTPSwiftea(FTPConnect):
	def __init__(self, host, user, password):
		FTPConnect.__init__(self, host, user, password)

	def send_index(self, index):
		with open(FILE_INDEX, 'w', encoding='utf-8') as myfile:
			myfile.write(index)
		rep = self.upload(FILE_INDEX, FTP_INDEX)
		if 'Error' in rep:
			# sending index failed
			speak("l'envoie de l'index a échoué : " + rep, 21)
			return 'error'
		else:
			speak(rep)
			return 'ok'

	def get_index(self, local_file_name, serveur_file_name):
		rep = self.download(local_file_name, serveur_file_name)
		if 'Error' in rep:
			# download index failed
			speak("erreur de téléchargement de l'index inversé : " + rep, 22)
			return None, 'error'
		else:
			with open(local_file_name, 'r', encoding='utf-8') as myfile:
				index = myfile.read()
			speak(rep)
			return index, rep

	def can_send(self): # not use at the moment, must be test
		"""Return True if the program can send to database, False if not.

		On the ftp serveur there is a file who contain data :
		- max requests per minute
		- number of requests did
		- the timestamp
		"""
		# Look if we can send data to database.
		# download and read the file
		# content is a dict
		# simple thing :
		if time() - content['timestamp'] >= 60:
			# the next minute
			content['number request'] = 0 # reset meter
			result = True
		else:
			# in the same minute
			if content['number requests'] + nb_request > content['max request']:
				result = False
			else:
				result = True
			content['number request'] += nb_request
		"""
		# Thing more complexe : return the number of requests who can do 
		if time() - content['timestamp'] >= 60:
			# the next minute
			content['number request'] = 0 # reset meter
			if nb_request <= content['max request']:
				result = nb_request
			else:
				result = content['max request']
		else:
			if content['number request'] + nb_request >= content['max request']:
				result = content['max request']
			else:
				result = nb_request
			content['number request'] += nb_request

		content['timestamp'] = time()
		"""

		# send the file

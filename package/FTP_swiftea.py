#!/usr/bin/

"""Class to manage the ftp connexion for swiftea."""

from package.FTP import FTPConnect
from package.data import FILE_INDEX, FTP_INDEX
from package.module import speak

__author__ = "Seva Nathan"

class FTPSwiftea(FTPConnect):
	"""docstring for FTPSwiftea"""
	def __init__(self, host, user, password):
		FTPConnect.__init__(self, host, user, password)

	def send_index(self, index):
		with open(FILE_INDEX, 'w', encoding='utf-8') as myfile:
			myfile.write(index)
		rep = self.upload(FILE_INDEX, FTP_INDEX)
		if 'Error' in rep:
			speak("l'envoie de l'index a échoué : " + rep, 21)
			return 'error'
		else:
			speak(rep)
			return 'ok'

	def get_index(self, local_file_name, serveur_file_name):
		rep = self.download(local_file_name, serveur_file_name)
		if 'Error' in rep:
			speak("erreur de téléchargement de l'index inversé : " + rep, 22)
			return None, 'error'
		else:
			with open(local_file_name, 'r', encoding='utf-8') as myfile:
				index = myfile.read()
			speak(rep)
			return index, rep

	def can_send(self):
		pass
		"""Look if we can send data to database.
		self.conexion()
		if self.connect is not None:
			with open(FILE_CAN_SEND, 'wb') as myfile:
				try:
					self.connect.retrbinary('RETR ' + FTP_CAN_SEND, myfile.write)
				except all_errors:
					speak('impossible de récupéré le fichier request.json (ftp)', 23)
					return False

			with open(FILE_CAN_SEND, 'r') as myfile:
				try:
					content = json.load(myfile)
				except ValueError:
					speak('impossible de récupéré le fichier request.json (local)', 24)
					return False

			with open('can_send.txt', 'a') as myfile:
				myfile.write(str(content) + '\n')

			# simple thing :
			if time() - content['timestamp'] >= 60:
				# the next minute
				content['number request'] = 0 # reset meter
				result = True

			else:
				# in the same minute
				if content['number request'] + nb_request > content['max request']:
					result = False
				else:
					result = True

				content['number request'] += nb_request

			# Thing more complexe (number of request allowed) : 
			if time() - content['timestamp'] >= 60:
				# the next minute
				content['number request'] = 0 # reset meter
				# dire 20 quoi qu'il arrive ou pas ?...
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
			#

			content['timestamp'] = time()

			with open(FILE_CAN_SEND, 'w') as myfile:
				json.dump(content, myfile)
			with open(FILE_CAN_SEND, 'rb') as myfile:
				self.connect.storbinary('STOR ' + FTP_CAN_SEND, myfile)

			self.quit_connection()

		else:
			speak('erreur de connexion au serveur ftp', 20)
			return ''

		"""

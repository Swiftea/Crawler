#!/usr/bin/python3

"""Class to manage the ftp connexion for swiftea."""

from os import path, listdir


from package.FTP import FTPConnect
from package.data import DIR_INDEX, FTP_INDEX, ALPHABET
from package.module import speak

__author__ = "Seva Nathan"

class FTPManager(FTPConnect):
	def __init__(self, host, user, password):
		FTPConnect.__init__(self, host, user, password)

	def get_inverted_index(self):
		to_download = self.get_indexs_to_download() # list of file to get index in ftp
		to_read = list() # list of to get index in local
		inverted_index = dict()
		self.connection()
		self.cwd(FTP_INDEX)
		response = 'No inverted-index'
		for letter_index in self.nlst():
			if letter_index in to_download:
				local_file_name = DIR_INDEX + letter_index
				server_file_name = FTP_INDEX + letter_index
				response = self.download(local_file_name, server_file_name)
				if 'Error' in response:
					speak('Failed to download inverted-index ' + server_file_name + ', ' + response, 22)
					return '0', None, 'error'
				else:
					with open(local_file_name, 'r', encoding='utf-8') as myfile:
						inverted_index[letter_index] = myfile.read()
					response = 'Transfer complete'
			else:
				to_read.append(letter_index)
				response = 'all inverted-indexs in local'
		return inverted_index, to_read, response

	def send_inverted_index(self, inverted_indexs):
		for index_letter in inverted_indexs:
			filename = DIR_INDEX + index_letter
			inverted_index = inverted_indexs[index_letter]
			with open(filename, 'w', encoding='utf-8') as myfile:
				myfile.write(inverted_index)
			response = self.upload(filename, FTP_INDEX + index_letter)
			if 'Error' in response:
				return response
		return None

	def get_indexs_to_download(self):
		to_download = list()
		list_indexs = listdir(DIR_INDEX) # local
		if len(list_indexs) == 27:
			self.connection()
			self.cwd(FTP_INDEX)
			for data in self.mlsd(facts=['size', 'type']):
				if data[1]['type'] == 'file':
					local_size = path.getsize(DIR_INDEX + data[0])
					if local_size != int(data[1]['size']):
						# different sizes, must download
						to_download.append(data[0])
		else:
			to_download = ALPHABET
			to_download.append('_')
		return to_download

	def can_send(self): # not use at the moment, must be tested
		"""Return True if the program can send to database, False if not.

		On the ftp server there is a file who contains data :
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

# other things :


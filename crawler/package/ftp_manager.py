#!/usr/bin/python3

from os import path, listdir


from package.FTP import FTPConnect
from package.data import DIR_INDEX, FTP_INDEX, ALPHABET
from package.module import speak

__author__ = "Seva Nathan"

class FTPManager(FTPConnect):
	"""Class to manage the ftp connexion for crawler"""
	def __init__(self, host, user, password):
		"""Build manager"""
		FTPConnect.__init__(self, host, user, password)

	def get_inverted_index(self, to_download):
		"""Get inverted-indexs

		:param to_download: inverted-indexs to download
		:type to_download: list
		:return: inverted-indexs and response: 'Transfer complete' or 'Failed' or 'No index on ftp'

		"""
		inverted_index = dict()
		self.connection()
		self.cwd(FTP_INDEX)
		speak('Indexs in ftp : ' + str(to_download))
		response = 'No index on ftp'
		for letter_index in self.nlst():
			if letter_index in to_download:
				local_filename = DIR_INDEX + letter_index
				server_filename = FTP_INDEX + letter_index
				response = self.download(local_filename, server_filename)
				if 'Error' in response:
					speak('Failed to download inverted-index ' + server_filename + ', ' + response, 22)
					return None, 'Failed', 'error'
				else:
					with open(local_filename, 'r', encoding='utf-8') as myfile:
						inverted_index[letter_index] = myfile.read()
					response = 'Transfer complete'
		return inverted_index, response

	def send_inverted_index(self, inverted_indexs):
		"""Send inverted-indexs

		:param inverted_indexs: inverted-indexs to send
		:type inverted_indexs: dict
		:return: response of sending or None if inverted_indexs is empty

		"""
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
		"""Compare inverted-indexs on ftp server and in local

		:return: list of inverted-indexs to download and those to read

		"""
		to_download = list() # list of files to get index in ftp
		to_read = list() # list of files to get index in local
		list_indexs = listdir(DIR_INDEX) # local
		self.connection()
		self.cwd(FTP_INDEX)
		if len(list_indexs) == 27: # can be improve
			self.cwd(FTP_INDEX)
			for data in self.mlsd(facts=['size', 'type']):
				if data[1]['type'] == 'file':
					local_size = path.getsize(DIR_INDEX + data[0])
					if int(data[1]['size']) > local_size:
						# different sizes, must download
						to_download.append(data[0])
					else: # int(data[1]['size']) <= local_size
						to_read.append(data[0])
		elif len(self.nlst()) == 27:
			to_download = ALPHABET
			to_download.append('_')
		self.quit_connection()
		return to_download, to_read

	def can_send(self): # not use at the moment, must be tested
		"""Return True if the program can send to database, False if not.

		On the ftp server there is a file who contains data :
		- max requests per minute
		- number of requests did
		- the timestamp

		Doesn't work

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


#!/usr/bin/python3

__author__ = "Seva Nathan"

from ftplib import FTP, all_errors


from package.data import TIMEOUT

class MyFtpError(Exception):
	"""How to use it: raise MyFtpError('my error message')"""
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class FTPConnect(FTP):
	"""Class to connect to a ftp server

	:param host: hostname of the ftp server
	:type host: str
	:param user: username to use for connexion
	:type user: str
	:param password: password to use for connexion
	:type password: str

	ideas:
	return the result if there is one
	return a tuple of string who describes all steps of the connexion and of transferts

	"""
	def __init__(self, host, user='', password=''):
		"""Build ftp manager"""
		FTP.__init__(self, timeout=TIMEOUT)
		self.host = host
		self.user = user
		self.password = password

	def connexion(self):
		try:
			# connexion to the ftp server :
			self.connect(self.host)
			# login :
			self.login(self.user, self.password)
		except all_errors as error:
			response = 'Failed to connect to server : ' + str(error)
		else:
			# use utf-8 encoding :
			self.sendcmd("OPTS UTF8 ON")
			response = self.getwelcome()

		return response

	def disconnect(self):
		try:
			response = self.quit()
		except all_errors as error:
			response = "Can't quit server : " + str(error)
		else:
			self.close()

		return response

	def upload(self, local_filename, server_filename):
		"""Upload a file into ftp server

		:param local_filename: local filename to upload
		:type local_filename: str
		:param server_filename: server filename to upload
		:type server_filename: str
		:return: response of server

		"""
		with open(local_filename, 'rb') as myfile:
			try:
				response = self.storbinary('STOR ' + server_filename, myfile)
			except all_errors as error:
				response = 'Failed to send file ' +	local_filename + ' : ' + str(error)
			else:
				response = 'Send file : ' + response
		return response

	def download(self, local_filename, server_filename):
		"""Download a file from ftp server

		:param local_filename: local filename to download
		:type local_filename: str
		:param server_filename: server filename to download
		:type server_filename: str
		:return: response of server

		"""
		with open(local_filename, 'wb') as myfile:
			try:
				response = self.retrbinary(
					'RETR ' + server_filename, myfile.write)
			except all_errors as error:
				response = 'Failed to download file ' +	server_filename + ' : ' + str(error)
			else:
				response = 'Download file ' + server_filename + ': ' + response
		return response

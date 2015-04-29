#!/usr/bin/python3

from ftplib import FTP, all_errors

from package.data import TIMEOUT

class MyFtpError(Exception):
	"""How to use it: raise MyFtpError('my error message')"""
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


class FTPManager(FTP):
	"""Class to connect to a ftp server more easily.

	:param host: hostname of the ftp server
	:type host: str
	:param user: username to use for connexion
	:type user: str
	:param password: password to use for connexion
	:type password: str
	"""
	def __init__(self, host, user='', password=''):
		"""Build ftp manager"""
		FTP.__init__(self, timeout=TIMEOUT)
		self.host = host
		self.user = user
		self.password = password


	def connexion(self):
		"""Connect to ftp server.

		Catch all_errors of ftplib. Use utf-8 encoding.

		:return: server welcome message
		"""
		try:
			# Connexion to ftp server:
			self.connect(self.host)
			# Login:
			self.login(self.user, self.password)
		except all_errors as error:
			response = 'Failed to connect to server : ' + str(error)
		else:
			# Use utf-8 encoding:
			self.sendcmd("OPTS UTF8 ON")
			response = self.getwelcome()
		return response


	def disconnect(self):
		"""Quit connexion to ftp server.

		Close it if an error occured while trying to quit it.

		:return: server goodbye message or error message
		"""
		try:
			response = self.quit()
		except all_errors as error:
			response = "Can't quit server : " + str(error)
		except AttributeError:
			response = "Connexion already exited."
		else:
			self.close()
		return response


	def upload(self, local_filename, server_filename):
		"""Upload a file into ftp server.

		The file to upload must exists.

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
		"""Download a file from ftp server.

		It creates the file to download.

		:param local_filename: local filename to create
		:type local_filename: str
		:param server_filename: server filename to download
		:type server_filename: str
		:return: server response message or error message
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

#!/usr/bin/env python3

"""Define a class that deal with the low level ftp manager."""


from socket import timeout
from ftplib import FTP, all_errors


from crawler.swiftea_bot.data import TIMEOUT


class MyFtpError(Exception):
	"""How to use it: raise MyFtpError('Error message')"""
	def __init__(self, value):
		self.value = value

	def __str__(self):
		return repr(self.value)


class FTPManager(FTP):
	"""Class to connect to a ftp server more easily.

	:param host: hostname of the ftp server
	:type host: str
	:param user: username to use for connection
	:type user: str
	:param password: password to use for connection
	:type password: str

	"""
	def __init__(self, host, user='', password='', port=21):
		"""Build ftp manager"""
		FTP.__init__(self, timeout=TIMEOUT)
		self.host = host
		self.user = user
		self.port = port
		self.password = password

	def connection(self):
		"""Connect to ftp server.

		Catch all_errors of ftplib. Use utf-8 encoding.

		:return: server welcome message

		"""
		try:
			# Connexion to ftp server:
			self.connect(self.host, self.port)
			# Login:
			self.login(self.user, self.password)
		except timeout:
			response = 'Timeout error'
		except all_errors as error:
			response = 'Failed to connect to server: ' + str(error)
		else:
			# Use utf-8 encoding:
			self.sendcmd("OPTS UTF8 ON")
			response = self.getwelcome()
		return response

	def disconnect(self):
		"""Quit connection to ftp server.

		Close it if an error occured while trying to quit it.

		:return: server goodbye message or error message

		"""
		try:
			response = self.quit()
		except all_errors as error:
			response = "Can't quit server: " + str(error)
		except AttributeError:
			response = 'Connexion already exited.'
		else:
			self.close()
		return response

	def cd(self, path):
		"""Set the current directory on the server.

		:param path: path to set
		:type path: str
		:return: sever response

		"""
		try:
			response = self.cwd(path)
		except all_errors as error:
			return 'Error: ' + str(error)
		else:
			return response

	def mkdir(self, dirname):
		"""Create a directory on the server.

		:param dirname: the directory path and name
		:type dirname: str
		:return: server response

		"""
		try:
			response = self.mkd(dirname)
		except all_errors as e:
			response = e
		finally:
			return response

	def listdir(self):
		"""Return the result of LIST command or
		a list whose first element is the error response."""
		try:
			result = self.nlst()
		except all_errors as error:
			return ['Error: ' + str(error)]
		else:
			if result != []:
				return result
			else:
				return ['Empty list']

	def listdir_attr(self, path='.', facts=[]):
		"""Return the result of mlsd command of ftplib or
		a list whose first element is the error response."""
		try:
			result = self.mlsd(path, facts)
		except  all_errors as error:
			return ['Error: ' + str(error)]
		else:
			return result

	def get_total_size(self, directory='.'):
	    size = 0
	    for filename in self.nlst(directory):
	        try:
	            self.cwd(filename)
	            size += self.get_total_size(filename)
	        except:
	            self.voidcmd('TYPE I')
	            size += self.size(filename)
	    return size

	def put(self, local_filename, server_filename):
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
				response = 'Failed to send file ' +	local_filename + ': ' + str(error)
			else:
				response = 'Send file: ' + response
		return response

	def get(self, local_filename, server_filename):
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
				response = 'Failed to download file ' +	server_filename + ': ' + str(error)
			else:
				response = 'Download file ' + server_filename + ': ' + response
		return response

	def countfiles(self, path='.'):
		"""Count the file in the given path

		:param path: path to count
		:type path: str
		:return: number of files

		"""
		nb_files = int()
		infos = self.infos_listdir(path, ['type', 'size'])
		for info in infos:
			if info[1]['type'] == 'dir':
				nb_files += self.countfiles(path + '/' + info[0])
			elif info[1]['type'] == 'file':
				nb_files += 1
		return nb_files

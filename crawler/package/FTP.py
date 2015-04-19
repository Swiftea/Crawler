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
		finally:
			return response

	def quit_connexion(self):
		try:
			response = self.quit()
		except all_errors as error:
			response = "Can't quit server : " + str(error)
		else:
			self.close()
		finally:
			return response

	def upload(self, local_filename, server_filename):
		"""Upload a file into ftp server

		:param local_filename: local filename to upload
		:type local_filename: str
		:param server_filename: server filename to upload
		:type server_filename: str
		:return: response of server

		"""
		response = self.connexion()
		if 'failed' in response:
			return response
		else:
			with open(local_filename, 'br') as myfile:
				try:
					response = self.storbinary(
						'STOR ' + server_filename, myfile)
				except all_errors as error:
					response = 'Failed to send file ' + \
						local_filename + ' : ' + str(error)
				else:
					response = 'Send file : ' + response
				finally:
					self.quit_connexion()
			return response

	def download(self, local_filename, server_filename):
		"""Download a file from ftp server

		:param local_filename: local filename to download
		:type local_filename: str
		:param server_filename: server filename to download
		:type server_filename: str
		:return: response of server

		"""
		response = self.connexion()
		if 'failed' in response:
			return response
		else:
			with open(local_filename, 'wb') as myfile:
				try:
					response = self.retrbinary(
						'RETR ' + server_filename, myfile.write)
				except all_errors as error:
					response = 'Failed to download file ' + \
						server_filename + ' : ' + str(error)
				else:
					response = 'Download file ' + server_filename + ': ' + response
				finally:
						self.quit_connexion()
			return response

	def list_dir(self):
		response = self.connexion()
		if 'failed' in response:
			return response
		else:
			try:
				response = self.retrlines('LIST')
			except all_errors as error:
				return None, 'Error : ' + str(error)
			else:
				return response, 'ok'
			finally:
				self.quit_connexion()

	def rename_file_dir(self, name1, name2):
		response = self.connexion()
		if 'failed' in response:
			return response
		else:
			try:
				response = self.rename(name1, name2)
			except all_errors as error:
				return 'Error : ' + str(error)
			else:
				return response
			finally:
				self.quit_connexion()

	def delete_file(self, file_name):
		response = self.connexion()
		if 'failed' in response:
			return response
		else:
			try:
				response = self.delete(file_name)
			except all_errors as error:
				return 'Error : ' + str(error)
			else:
				return response
			finally:
				self.quit_connexion()

	def make_dir(self, name_dir): # except file exist
		response = self.connexion()
		if 'failed' in response:
			return response
		else:
			try:
				response = self.mkd(dir_name)
			except all_errors as error:
				return 'Error : ' + str(error)
			else:
				return response
			finally:
				self.quit_connexion()

	def del_dir(self, dir_name):
		response = self.connexion()
		if 'failed' in response:
			return response
		else:
			try:
				response  = self.rmd(dir_name)
			except all_errors as error:
				return 'Error : ' + str(error)
			else:
				return response
			finally:
				self.quit_connexion()

	def send_func(self, comand):
		response = self.connexion()
		if 'failed' in response:
			return response
		else:
			try:
				response = self.sendcmd(comand)
			except all_errors as error:
				return 'Error : ' + str(error)
			else:
				return response
			finally:
				self.quit_connexion()

	def stop_sending(self):
		self.connect.abort() # mieu à faire ?
		return 'sending stoped'

	def change_dir(self, path):
		response = self.connexion()
		if 'failed' in response:
			return response
		else:
			try:
				response = self.cwd(path)
			except all_errors as error:
				return 'Error : ' + str(error)
			finally:
				self.quit_connexion()

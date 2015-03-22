#!/usr/bin/python3

"""Module to connect to a ftp server."""

__author__ = "Seva Nathan"

from ftplib import FTP, all_errors

class MyFtpError(Exception):
	"""How use it : raise MyFtpError('my error message')"""
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class FTPConnect(FTP):
	def __init__(self, host, user='', password=''):
		"""Build the ftp managment.

		host : hostname of the ftp serveur
		user : username to use for connection
		password : password to use for connection

		ideas :
		return the result if there is one
		return a tuple of string who descibe all steps of the connection and of transferts

		"""
		FTP.__init__(self)
		self.host = host
		self.user = user
		self.password = password

	def connection(self):
		try:
			# connection to the ftp serveur :
			self.connect(self.host)
			# loging in :
			self.login(self.user, self.password)
		except all_errors as error:
			rep = 'Failed to connect to server : ' + str(error)
		else:
			# use utf-8 encoding :
			self.sendcmd("OPTS UTF8 ON")
			rep = self.getwelcome()
		finally:
			return rep

	def quit_connection(self):
		try:
			rep = self.quit()
		except all_errors as error:
			rep = "Can't quit server : " + str(error)
		else:
			self.close()
		finally:
			return rep

	def upload(self, local_file_name, serveur_file_name):
		rep = self.connection()
		if 'failed' in rep:
			return rep
		else:
			with open(local_file_name, 'br') as myfile:
				try:
					rep = self.storbinary(
						'STOR ' + serveur_file_name, myfile)
				except all_errors as error:
					rep = 'Failed to send file ' + \
						local_file_name + ' : ' + str(error)
				else:
					rep = 'Send file : ' + rep
				finally:
					self.quit_connection()
			return rep

	def download(self, local_file_name, serveur_file_name):
		rep = self.connection()
		if 'failed' in rep:
			return rep
		else:
			with open(local_file_name, 'wb') as myfile:
				try:
					rep = self.retrbinary(
						'RETR ' + serveur_file_name, myfile.write)
				except all_errors as error:
					rep = 'Failed to download file ' + \
						serveur_file_name + ' : ' + str(error)
				else:
					rep = 'Download file : ' + rep
				finally:
						self.quit_connection()
			return rep

	def list_dir(self):
		rep = self.connection()
		if 'failed' in rep:
			return rep
		else:
			try:
				rep = self.retrlines('LIST')
			except all_errors as error:
				return None, 'Error : ' + str(error)
			else:
				return rep, 'ok'
			finally:
				self.quit_connection()

	def rename_file_dir(self, name1, name2):
		rep = self.connection()
		if 'failed' in rep:
			return rep
		else:
			try:
				rep = self.rename(name1, name2)
			except all_errors as error:
				return 'Error : ' + str(error)
			else:
				return rep
			finally:
				self.quit_connection()

	def delete_file(self, file_name):
		rep = self.connection()
		if 'failed' in rep:
			return rep
		else:
			try:
				rep = self.delete(file_name)
			except all_errors as error:
				return 'Error : ' + str(error)
			else:
				return rep
			finally:
				self.quit_connection()

	def make_dir(self, name_dir): # except file exist
		rep = self.connection()
		if 'failed' in rep:
			return rep
		else:
			try:
				rep = self.mkd(dir_name)
			except all_errors as error:
				return 'Error : ' + str(error)
			else:
				return rep
			finally:
				self.quit_connection()

	def del_dir(self, dir_name):
		rep = self.connection()
		if 'failed' in rep:
			return rep
		else:
			try:
				rep  = self.rmd(dir_name)
			except all_errors as error:
				return 'Error : ' + str(error)
			else:
				return rep
			finally:
				self.quit_connection()

	def send_func(self, comand):
		rep = self.connection()
		if 'failed' in rep:
			return rep
		else:
			try:
				rep = self.sendcmd(comand)
			except all_errors as error:
				return 'Error : ' + str(error)
			else:
				return rep
			finally:
				self.quit_connection()

	def stop_sending(self):
		self.connect.abort() # mieu à faire ?
		return 'sending stoped'

	def change_dir(self, path):
		rep = self.connection()
		if 'failed' in rep:
			return rep
		else:
			try:
				rep = self.cwd(path)
			except all_errors as error:
				return 'Error : ' + str(error)
			finally:
				self.quit_connection()

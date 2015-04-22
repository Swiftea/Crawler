#!/usr/bin/python3

import socket


import pymysql # for database access

from package.data import TIMEOUT

__author__ = "Seva Nathan"

class DatabaseManager(object):
	"""Class to manage database\n\n
	How to: create a subclass\n
	result, response = self.send_comand(command, data=tuple(), all=False)\n
	where result are data asked

	:param host: hostname of the ftp server
	:type host: str
	:param user: username to use for connexion
	:type user: str
	:param password: password to use for connexion
	:type password: str
	:param name: name of database
	:type name: str

	"""
	def __init__(self, host, user, password, name):
		"""Build database manager"""
		self.host = host # hostname
		self.user = user # username
		self.password = password # password
		self.name = name # database name
		self.cursor = self.conn = None

	def connexion(self):
		"""Connect to database"""
		try:
			self.conn = pymysql.connect(host=self.host,
				user=self.user,
				passwd=self.password,
				db=self.name,
				use_unicode=True,
				charset='utf8',
				connect_timeout=TIMEOUT)
		except pymysql.err.OperationalError as error:
			response = 'Connexion error : ' + str(error)
		except socket.timeout:
			response = 'Connexion error (socket.timeout:)'
		else:
			self.cursor = self.conn.cursor() # cursor building
			response = 'Connected to database'

		return response

	def close_connexion(self):
		"""Close the database connexion"""
		self.cursor.close()
		self.conn.close()

	def send_command(self, command, data=tuple(), fetchall=False):
		"""Send a query to database

		:param data: data attached to given query
		:type data: tuple
		:param fetchall: True if return all results
		:type fetchall: bool
		:return: result of the query and status message.

		"""
		response = self.connexion()
		if response != 'Connected to database':
			return None, response
		else:
			try:
				self.cursor.execute(command, data)
				if fetchall:
					result = self.cursor.fetchall()
				else:
					result = self.cursor.fetchone()
			except pymysql.err.OperationalError:
				result = None
				response = 'Connexion error (err.OperationalError)'
			except socket.timeout:
				result = None
				response = 'Connexion error (socket.timeout)'
			else:
				response = 'Send command : ok'

			self.close_connexion()
			return result, response

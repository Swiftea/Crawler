#!/usr/bin/python3

import pymysql

from swiftea_bot.data import TIMEOUT

class DatabaseManager(object):
	"""Class to manage query to Database using PyMySQL.

	How to: create a subclass

	result, response = self.send_comand(command, data=tuple(), all=False)\n
	if 'error' in response:\n
	\tprint('An error occured.')

	where result are data asked and response a message.

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
		self.host = host  # Hostname
		self.user = user  # Username
		self.password = password  # Password
		self.name = name  # Database name
		self.cursor = self.conn = None

	def set_name(self, name):
		"""Set base name

		:param name: new base name
		:type name: str

		"""
		self.name = name


	def connexion(self):
		"""Connect to database."""
		try:
			self.conn = pymysql.connect(host=self.host,
				user=self.user,
				passwd=self.password,
				db=self.name,
				use_unicode=True,
				charset='utf8',
				connect_timeout=TIMEOUT)
		except pymysql.err.OperationalError as error:
			response = 'Connexion error: ' + str(error)
		else:
			self.cursor = self.conn.cursor()  # Cursor building
			response = 'Connected to database'

		return response


	def close_connexion(self):
		"""Close database connexion."""
		self.cursor.close()
		self.conn.close()


	def send_command(self, command, data=tuple(), fetchall=False):
		"""Send a query to database.

		Catch timeout and OperationalError.

		:param data: data attached to query
		:type data: tuple
		:param fetchall: True if return all results
		:type fetchall: bool
		:return: result of the query and status message

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
				response = 'Operational error'
			else:
				response = 'Send command: ok'

			self.close_connexion()
			return result, response

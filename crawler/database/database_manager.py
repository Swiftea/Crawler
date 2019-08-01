#!/usr/bin/env python3

"""Define a class that deal with the low level database manager."""

import pymysql

from crawler.swiftea_bot.data import TIMEOUT


class DatabaseManager(object):
	"""Class to manage queries to the database using PyMySQL.

	How to: create a subclass

	result, response = self.send_comand(command, data=tuple(), all=False)\n
	if 'error' in response:\n
	\tprint('An error occured.')

	where result are data asked and response a message.

	:param host: hostname of the db server
	:type host: str
	:param user: username to use for connection
	:type user: str
	:param password: password to use for connection
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
		self.co = False  # True if connected to database

	def set_name(self, name):
		"""Set base name

		:param name: new base name
		:type name: str

		"""
		self.name = name

	def connection(self):
		"""Connect to database."""
		try:
			self.conn = pymysql.connect(host=self.host,
				user=self.user,
				passwd=self.password,
				db=self.name,
				use_unicode=True,
				charset='utf8mb4',
				connect_timeout=TIMEOUT)
		except pymysql.err.OperationalError as error:
			response = 'Connection error: ' + str(error)
		else:
			self.cursor = self.conn.cursor()  # Cursor building
			response = 'Connected to database'
			self.co = True

		return response

	def close_connection(self):
		"""Close database connection."""
		self.cursor.close()
		self.conn.close()
		self.co = False

	def send_command(self, command, data=tuple(), fetchall=False):
		"""Send a query to database.

		Catch timeout and OperationalError.

		:param data: data attached to query
		:type data: tuple
		:param fetchall: True if return all results
		:type fetchall: bool
		:return: result of the query and status message

		"""
		if not self.co:
			co = True
			response = self.connection()
			if response != 'Connected to database':
				return None, response
		else:
			co = False
		try:
			response = self.cursor.execute(command, data)
			if fetchall:
				result = self.cursor.fetchall()
			else:
				result = self.cursor.fetchone()
		except (pymysql.err.OperationalError, pymysql.err.ProgrammingError) as e:
			result = None
			response = 'Mysql error: ' + str(e)
		else:
			response = 'Send command: ok'

		self.conn.commit()  # addded in March 2018 to fix `insert fail but no error`

		if co:
			self.close_connection()
		return result, [0, str(response)]

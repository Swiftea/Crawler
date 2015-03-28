#!/usr/bin/python3

"""Module of management of database."""

import pymysql # for database access

from package.data import TIMEOUT

__author__ = "Seva Nathan"

class DatabaseManager:
	"""Using :

	With creating a subclass :
	result, response = self.send_comand(command, data=tuple(), all=False)
	result are data asked
	response is a message

	"""
	def __init__(self, host, user, password, name):
		"""Build the class."""
		self.host = host # hostname
		self.user = user # username
		self.password = password # password
		self.name = name # database name
		self.cursor, self.connexion = None, None

	def connection(self):
		"""Connect to database."""
		try:
			self.connexion = pymysql.connect(host=self.host,
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
			self.cursor = self.connexion.cursor() # cursor building
			response = 'Connected to database'
		finally:
			return response

	def close_connection(self):
		"""Close the database connection."""
		self.cursor.close()
		self.connexion.close()

	def send_command(self, command, data=tuple(), all=False):
		"""Return the result of the comand and the status message.

		data must be a variable or a tuple of variables.

		"""
		response = self.connection()
		if response != 'Connected to database':
			return None, response
		else:
			try:
				self.cursor.execute(command, data)
				if all:
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
			finally:
				self.close_connection()
				return result, response

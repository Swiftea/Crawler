#!/usr/bin/python3

"""Module of management of database."""

import socket # for timeout error


import pymysql # for database access

__author__ = "Seva Nathan"

class DataBase:
	"""Using :

	With creating a subclass :
	result, rep = self.send_comand(comand, data=tuple())
	result is the data asked
	rep is a message

	"""
	def __init__(self, host, user, password, base):
		"""Build the class."""
		self.host = host # hostname
		self.user = user # username
		self.password = password # password
		self.base = base # database name
		self.cur = None # cursor

	def connection(self):
		"""Connect to database."""
		try:
			self.conn = pymysql.connect(host=self.host,
				user=self.user,
				passwd=self.password,
				db=self.base,
				use_unicode=True,
				charset='utf8')
		except pymysql.err.OperationalError as error:
			rep = 'Connection error : ' + str(error)
		except socket.timeout:
			rep = 'Connection error (socket.timeout:)'
		else:
			self.cur = self.conn.cursor() # cursor building
			rep = 'Connected to data base'
		finally:
			return rep

	def close_connection(self):
		"""Close the database connection."""
		self.cur.close()
		self.conn.close()

	def send_command(self, comand, data=tuple()):
		"""Return the result of the comand and the status message.

		data must be a variable or a tuple of variables.

		"""
		rep = self.connection()
		if 'error' in rep:
			return None, rep
		else:
			try:
				self.cur.execute(comand, data)
				result = self.cur.fetchall()
			except pymysql.err.OperationalError:
				result = None
				rep = 'Connection error (err.OperationalError)'
			except socket.timeout:
				result = None
				rep = 'Connection error (socket.timeout)'
			else:
				rep = 'Send comand : ok'
			finally:
				self.close_connection()
				return result, rep

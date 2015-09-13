#!/usr/bin/python3

from socket import timeout
import paramiko

from swiftea_bot.data import TIMEOUT


class SFTPManager(FTP):
	"""Class to connect to a ftp server more easily.

	:param host: hostname server
	:type host: str
	:param user: username to use for connexion
	:type user: str
	:param password: password to use for connexion
	:type password: str

	"""
	def __init__(self, host, user='', password=''):
		FTP.__init__(self, timeout=TIMEOUT)
		self.host = host
		self.user = user
		self.password = password

        self.transport = None
        self.sftp = None

	def connexion(self):
		"""Connect to server.

		Catch Exception of ftplib. Use utf-8 encoding.

		"""
		try:
            self.transport = paramiko.Transport(self.host)
            self.transport.connect(username=self.user, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
		except timeout:
			response = 'Timeout error'
		except Exception as error:
			response = 'Failed to connect to server: ' + str(error)
        else:
            response = 'Connected'
		return response

	def disconnect(self):
		"""Quit connexion to ftp server.

		Close it if an error occured while trying to quit it.

		:return: server goodbye message or error message

		"""
		self.sftp.close()
		self.transport.close()
        self.sftp = None
		self.transport = None


	def cd(self, path):
		"""Set the current directory on the server.

		:param path: path to set
		:type path: str
		:return: sever response

		"""
		try:
			self.sftp.chdir(path)
		except Exception as error:
			return 'Error: ' + str(error)
		else:
			return 'ok'

	def listdir(self, path='.'):
		"""Return a list containing the names of the entries in the given path."""
		try:
			result = self.sftp.listdir(path)
		except Exception as error:
			return ['Error: ' + str(error)]
		else:
			return result

	def listdir_attr(self, path='.'):
		try:
			result = self.sftp.listdir_attr(path)
		except Exception as error:
			return 'Error: ' + str(error)
		else:
			return result

	def upload(self, local_filename, server_filename):
		"""Upload a file into server.

		:param local_filename: local filename to upload
		:type local_filename: str
		:param server_filename: server filename to upload
		:type server_filename: str
		:return: response of server

		"""
		try:
            self.sftp.put(local_filename, server_filename)
        except Exception as error:
            return 'Error: ' + str(error)
        else:
            return 'Ok'

	def download(self, local_filename, server_filename):
		"""Download a file from ftp server.

		:param local_filename: local filename to create
		:type local_filename: str
		:param server_filename: server filename to download
		:type server_filename: str
		:return: server response message or error message

		"""
		try:
            self.sftp.get(server_filename, local_filename)
        except Exception as error:
            return 'Error: ' + str(error)
        else:
            return 'Ok'

	def countfiles(self, path='.'):
		"""Count the file in the given path

		:param path: path to count
		:type path: str
		:return: number of files

		"""
		nb_files = int()
		infos = self.infos_listdir(path)
		for info in infos:
			if info[1]['type'] == 'dir':
				nb_files += self.countfiles(path + '/' + info[0])
			elif info[1]['type'] == 'file':
				nb_files += 1
		return nb_files

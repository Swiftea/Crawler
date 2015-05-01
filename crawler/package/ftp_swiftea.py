#!/usr/bin/python3

from os import path, mkdir
import json

from package.ftp_manager import FTPManager
from package.data import DIR_INDEX, FTP_INDEX
from package.module import tell

class FTPSwiftea(FTPManager):
	"""Class to manage the ftp connexion for crawler."""
	def __init__(self, host, user, password):
		FTPManager.__init__(self, host, user, password)


	def get_inverted_index(self):
		"""Get inverted-index.

		:return: inverted-index and True if an error occured

		"""
		tell('Get inverted-index from server')
		error_msg = '', True
		inverted_index = dict()
		self.connexion()
		if self.cd(FTP_INDEX).startswith('Error'): return error_msg

		list_language = self.listdir()
		if list_language[0].startswith('Error'): return error_msg
		for language in list_language:
			if self.cd(language).startswith('Error'): return error_msg
			if not path.isdir(DIR_INDEX + language):
				mkdir(DIR_INDEX + language)
			inverted_index[language] = dict()

			list_first_letter = self.listdir()
			if list_first_letter[0].startswith('Error'): return error_msg
			for first_letter in list_first_letter:
				if self.cd(first_letter).startswith('Error'): return error_msg
				if not path.isdir(DIR_INDEX + language + '/' + first_letter):
					mkdir(DIR_INDEX +  language + '/' + first_letter)
				inverted_index[language][first_letter] = dict()

				list_filename = self.listdir()
				if list_filename[0].startswith('Error'): return error_msg
				for filename in list_filename:
					path_index = language + '/' + first_letter + '/' + filename
					response = self.download(DIR_INDEX + path_index, filename)
					if 'Error' in response:
						return path_index + ': ' + response
					else:
						with open(DIR_INDEX + path_index, 'r', encoding='utf-8') as myfile:
							inverted_index[language][first_letter][filename[:-4]] = json.load(myfile)
				if self.cd('..').startswith('Error'): return error_msg
			if self.cd('..').startswith('Error'): return error_msg
		self.disconnect()
		if inverted_index == dict():
			tell('No inverted-index on ftp', severity=0)
		else:
			tell('Transfer complete', severity=0)
		return inverted_index, False

	def send_inverted_index(self, inverted_index):
		"""Send inverted-index.

		:param inverted_index: inverted-index to send
		:type inverted_index: dict
		:return: True if an error occured

		"""
		tell('Send inverted-index')
		self.connexion()
		if self.cd(FTP_INDEX).startswith('Error'): return ''
		for language in inverted_index:
			list_language = self.listdir()
			if list_language[0].startswith('Error'): return ''
			if language not in list_language:
				self.mkd(language)
			if not path.isdir(DIR_INDEX + language):
				mkdir(DIR_INDEX + language)
			if self.cd(language).startswith('Error'): return ''
			for first_letter in inverted_index[language]:
				list_first_letter = self.listdir()
				if list_first_letter[0].startswith('Error'): return ''
				if first_letter not in list_first_letter:
					self.mkd(first_letter)
				if not path.isdir(DIR_INDEX + language + '/' + first_letter):
					mkdir(DIR_INDEX + language + '/' + first_letter)
				if self.cd(first_letter).startswith('Error'): return ''
				for two_letters in inverted_index[language][first_letter]:
					index = inverted_index[language][first_letter][two_letters]
					path_index = language + '/' + first_letter + '/' + two_letters + '.sif'
					with open(DIR_INDEX + path_index, 'w', encoding='utf-8') as myfile:
						json.dump(index, myfile, ensure_ascii=False)
					response = self.upload(DIR_INDEX + path_index, two_letters + '.sif')
					if 'Error' in response:
						return path_index + ': ' + response
				if self.cd('..').startswith('Error'): return ''
			if self.cd('..').startswith('Error'): return ''
		self.disconnect()
		tell('Transfer complete', severity=0)
		return False


	def compare_indexs(self):
		"""Compare inverted-index in local and in server.

		:return: True if must dowload from server

		"""
		local_file = DIR_INDEX + 'FR/' + 'C/' + 'co.sif'
		if path.exists(local_file):
			local_size = path.getsize(local_file)
			self.connexion()
			if self.cd(FTP_INDEX).startswith('Error'): return False
			server_size = 0
			list_language = self.listdir()
			if list_language[0].startswith('Error'): return True
			if 'FR' in list_language:
				if self.cd('FR').startswith('Error'): return False
				list_first_letter = self.listdir()
				if list_first_letter[0].startswith('Error'): return False
				if 'C' in list_first_letter:
					if self.cd('C').startswith('Error'): return False
					infos_filename = self.infos_listdir(facts=['type', 'size'])
					if isinstance(infos_filename, str): return False
					for data in infos_filename:
						if data[0] == 'co.sif':
							server_size = int(data[1]['size'])
			self.disconnect()
			if local_size < server_size:
				return True
			else:
				return False
		else:
			return True

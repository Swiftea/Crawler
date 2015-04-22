#!/usr/bin/python3

from os import path, mkdir
import json


from package.FTP import FTPConnect
from package.data import DIR_INDEX, FTP_INDEX
from package.module import speak

__author__ = "Seva Nathan"

class FTPManager(FTPConnect):
	"""Class to manage the ftp connexion for crawler"""
	def __init__(self, host, user, password):
		"""Build manager"""
		FTPConnect.__init__(self, host, user, password)

	def get_inverted_index(self):
		"""Get inverted-indexs

		:return: inverted-indexs and True if an error occured

		"""
		speak('Get inverted-indexs')
		inverted_index = dict()
		self.connexion()
		self.cwd(FTP_INDEX)

		for language in self.nlst():
			self.cwd(language)
			if not path.isdir(DIR_INDEX + language):
				mkdir(DIR_INDEX + language)
			inverted_index[language] = dict()

			for first_letter in self.nlst():
				self.cwd(first_letter)
				if not path.isdir(DIR_INDEX + language + '/' + first_letter):
					mkdir(DIR_INDEX +  language + '/' + first_letter)
				inverted_index[language][first_letter] = dict()

				for filename in self.nlst():
					path_index = language + '/' + first_letter + '/' + filename
					response = self.download(DIR_INDEX + path_index, filename)
					if 'Error' in response:
						speak('Failed to download inverted-index ' + path_index + ', ' + response, 22)
						return None, True
					else:
						with open(DIR_INDEX + path_index, 'r', encoding='utf-8') as myfile:
							inverted_index[language][first_letter][filename] = json.load(myfile)
				self.cwd('..')
			self.cwd('..')
		self.disconnect()
		if inverted_index == dict():
			speak('No inverted-index on ftp')
		else:
			speak('Transfer complete')
		return inverted_index, False

	def send_inverted_index(self, inverted_index):
		"""Send inverted-indexs

		:param inverted_index: inverted-indexs to send
		:type inverted_index: dict
		:return: True if an error occured

		"""
		speak('Send inverted-indexs')
		self.connexion()
		self.cwd(FTP_INDEX)
		for language in inverted_index:
			if language not in self.nlst():
				self.mkd(language)
			if not path.isdir(DIR_INDEX + language):
				mkdir(DIR_INDEX + language)
			self.cwd(language)
			for first_letter in inverted_index[language]:
				if first_letter not in self.nlst():
					self.mkd(first_letter)
				if not path.isdir(DIR_INDEX + language + '/' + first_letter):
					mkdir(DIR_INDEX + language + '/' + first_letter)
				self.cwd(first_letter)
				for two_letters in inverted_index[language][first_letter]:
					index = inverted_index[language][first_letter][two_letters]
					path_index = language + '/' + first_letter + '/' + two_letters + '.sif'
					with open(DIR_INDEX + path_index, 'w', encoding='utf-8') as myfile:
						json.dump(index, myfile, ensure_ascii=False)
					response = self.upload(DIR_INDEX + path_index, two_letters + '.sif')
					if 'Error' in response:
						speak('Failed to send inverted-indexs ' + path_index + ', ' + response, 21)
						return True
				self.cwd('..')
			self.cwd('..')
		self.disconnect()
		speak('Transfer complete')
		return False

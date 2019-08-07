#!/usr/bin/env python3

"""Define a class that deal with the high level ftp manager."""


from os import mkdir, path, walk
import json


from crawler.index.index import count_files_index
#from crawler.index.ftp_manager import SFTPManager as FTPManager
from crawler.index.ftp_manager import FTPManager
from crawler.swiftea_bot.module import tell


class FTPSwiftea(FTPManager):
	"""Class to manage the ftp connection for crawler."""
	def __init__(self, config):
		host = config['FTP_HOST']
		user = config['FTP_USER']
		password = config['FTP_PASSWORD']
		port = config['FTP_PORT']
		self.FTP_INDEX = config['FTP_INDEX']
		self.FTP_DATA = config['FTP_DATA']
		self.DIR_INDEX = config['DIR_INDEX']
		FTPManager.__init__(self, host, user, password, port)

	def set_ftp_index(self, FTP_INDEX):
		self.FTP_INDEX = FTP_INDEX

	def get_inverted_index(self):
		"""Get inverted-index.

		:return: inverted-index and True if an error occured

		"""
		tell('Get inverted-index from server')
		self.downuploaded_files = 0
		inverted_index = dict()
		self.connection()
		self.cd(self.FTP_INDEX)
		self.nb_files = self.countfiles()  # Count files on server (prepare to download)
		list_language = self.listdir()

		for language in list_language:
			self.cd(language)
			if not path.isdir(self.DIR_INDEX + language):
				mkdir(self.DIR_INDEX + language)
			inverted_index[language] = dict()
			list_first_letter = self.listdir()
			for first_letter in list_first_letter:
				self.tell_progress(False)
				self.cd(first_letter)
				if not path.isdir(self.DIR_INDEX + language + '/' + first_letter):
					mkdir(self.DIR_INDEX +  language + '/' + first_letter)
				inverted_index[language][first_letter] = dict()
				list_filename = self.listdir()
				for filename in list_filename:
					inverted_index[language][first_letter][filename[:-4]] = self.download(language, first_letter, filename)

				self.cd('..')
			self.cd('..')

		self.disconnect()
		if inverted_index == dict():
			tell('No inverted-index on server', severity=0)
		else:
			tell('Transfer complete', severity=0)
		return inverted_index

	def send_inverted_index(self, inverted_index):
		"""Send inverted-index.

		:param inverted_index: inverted-index to send
		:type inverted_index: dict
		:return: True if an error occured

		"""
		tell('send inverted-index')
		self.downuploaded_files = 0
		self.nb_files = count_files_index(inverted_index)  # Count files from index (prepare to upload)
		self.connection()
		files = self.listdir()
		if self.FTP_INDEX not in files:
			self.mkdir(self.FTP_INDEX)
		self.cd(self.FTP_INDEX)
		tell('go to ' + self.FTP_INDEX)

		for language in inverted_index:
			list_language = self.listdir()
			if language not in list_language:
				self.mkdir(language)
			self.cd(language)
			tell('go to ' + language)
			for first_letter in inverted_index[language]:
				self.tell_progress()
				list_first_letter = self.listdir()
				if first_letter not in list_first_letter:
					self.mkdir(first_letter)

				self.cd(first_letter)
				tell('go to ' + first_letter)
				for two_letters in inverted_index[language][first_letter]:
					index = inverted_index[language][first_letter][two_letters]
					self.upload(language, first_letter, two_letters, index)

				self.cd('..')
				tell('go back')
			self.cd('..')
			tell('go back')

		self.disconnect()
		tell('Transfer complete', severity=0)
		return False

	def download(self, language, first_letter, filename):
		self.downuploaded_files += 1
		FTP_INDEX = language + '/' + first_letter + '/' + filename
		self.get(self.DIR_INDEX + FTP_INDEX, filename)
		with open(self.DIR_INDEX + FTP_INDEX, 'r', encoding='utf-8') as myfile:
			return json.load(myfile)

	def upload(self, language, first_letter, two_letters, index):
		FTP_INDEX = language + '/' + first_letter + '/' + two_letters + '.sif'
		tell('uploading {} in {}'.format(self.DIR_INDEX + FTP_INDEX, two_letters + '.sif'))
		self.put(self.DIR_INDEX + FTP_INDEX, two_letters + '.sif')
		self.downuploaded_files += 1

	def tell_progress(self, upload=True):
		message = 'Uploading' if upload else 'Downloading'
		if self.nb_files != 0:
			percent = round(self.downuploaded_files * 100 / self.nb_files, 2)
			message += ' {}% ({}/{})'.format(percent, self.downuploaded_files, self.nb_files)
			tell(message)
		else:
			tell('No progress data')

	def download_lists_words(self):
		"""Download stopwords and badwords."""
		tell('download list of words')
		self.connection()
		for filename in ['en.stopwords.txt', 'fr.stopwords.txt', 'en.badwords.txt', 'fr.badwords.txt']:
			type_ = filename[3:-4] + '/'
			self.cd(self.FTP_DATA + type_)
			self.get(type_ + filename, filename)
		self.disconnect()

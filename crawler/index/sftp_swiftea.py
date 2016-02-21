#!/usr/bin/python3

from os import mkdir
import json
from os import path

from index.index import count_files_index
from index.sftp_manager import SFTPManager
from swiftea_bot.data import DIR_INDEX, SFTP_INDEX, DIR_DATA
from swiftea_bot.module import tell

class SFTPSwiftea(SFTPManager):
	"""Class to manage the sftp connexion for crawler."""
	def __init__(self, host, user, password):
		SFTPManager.__init__(self, host, user, password)
		self.sftp_index = SFTP_INDEX

	def set_sftp_index(self, sftp_index):
		self.sftp_index = sftp_index


	def get_inverted_index(self):
		"""Get inverted-index.

		:return: inverted-index and True if an error occured

		"""
		tell('Get inverted-index from server')
		self.downuploaded_files = 0
		inverted_index = dict()
		self.connexion()
		self.cd(self.sftp_index)
		self.nb_files = self.countfiles()  # Count files on server (prepare to download)
		list_language = self.listdir()

		for language in list_language:
			self.cd(language)
			if not path.isdir(DIR_INDEX + language):
				mkdir(DIR_INDEX + language)
			inverted_index[language] = dict()
			list_first_letter = self.listdir()
			for first_letter in list_first_letter:
				self.tell_progress(False)
				self.cd(first_letter)
				if not path.isdir(DIR_INDEX + language + '/' + first_letter):
					mkdir(DIR_INDEX +  language + '/' + first_letter)
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
		self.connexion()
		self.cd(self.sftp_index)

		for language in inverted_index:
			list_language = self.listdir()
			if language not in list_language:
				self.mkdir(language)
			if not path.isdir(DIR_INDEX + language):
				mkdir(DIR_INDEX + language)
			self.cd(language)
			for first_letter in inverted_index[language]:
				self.tell_progress()
				list_first_letter = self.listdir()
				if first_letter not in list_first_letter:
					self.mkdir(first_letter)
				if not path.isdir(DIR_INDEX + language + '/' + first_letter):
					mkdir(DIR_INDEX + language + '/' + first_letter)

				self.cd(first_letter)
				for two_letters in inverted_index[language][first_letter]:
					index = inverted_index[language][first_letter][two_letters]
					self.upload(language, first_letter, two_letters, index)

				self.cd('..')
			self.cd('..')

		self.disconnect()
		tell('Transfer complete', severity=0)
		return False


	def download(self, language, first_letter, filename):
		self.downuploaded_files += 1
		path_index = language + '/' + first_letter + '/' + filename
		self.get(DIR_INDEX + path_index, filename)
		with open(DIR_INDEX + path_index, 'r', encoding='utf-8') as myfile:
			return json.load(myfile)

	def upload(self, language, first_letter, two_letters, index):
		self.downuploaded_files += 1
		path_index = language + '/' + first_letter + '/' + two_letters + '.sif'
		with open(DIR_INDEX + path_index, 'w', encoding='utf-8') as myfile:
			json.dump(index, myfile, ensure_ascii=False)
		self.put(DIR_INDEX + path_index, two_letters + '.sif')


	def tell_progress(self, upload=True):
		message = 'Uploading' if upload else 'Downloading'
		if self.nb_files != 0:
			percent = round(self.downuploaded_files * 100 / self.nb_files, 2)
			message += ' {}% ({}/{})'.format(percent, self.downuploaded_files, self.nb_files)
			tell(message)
		else:
			tell('No progress data')


	def compare_indexs(self):
		"""Compare inverted-index in local and in server.

		:return: True if must download from server

		"""
		local_file = DIR_INDEX + 'FR/' + 'C/' + 'co.sif'
		if path.exists(local_file):
			local_size = path.getsize(local_file)
			self.connexion()
			self.cd(self.sftp_index)
			server_size = 0
			list_language = self.listdir()
			if 'FR' in list_language:
				self.cd('FR')
				list_first_letter = self.listdir()
				if 'C' in list_first_letter:
					self.cd('C')
					infos_filename = self.listdir_attr()
					for data in infos_filename:
						if data.filename == 'co.sif':
							server_size = data.st_size
			self.disconnect()
			if local_size < server_size:
				return True
			else:
				return False
		else:
			return True

	def download_lists_words(self):
		"""Download stopwords and badwords."""
		tell('download list of words')
		self.connexion()
		for filename in ['en.stopwords.txt', 'fr.stopwords.txt', 'en.badwords.txt', 'fr.badwords.txt']:
			type_ = filename[3:-4] + '/'
			self.cd('/var/www/html/data/' + type_)
			self.get(DIR_DATA + type_ + filename, filename)
		self.disconnect()

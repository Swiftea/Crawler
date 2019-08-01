#!/usr/bin/env python3

"""Define a class that deal with the high level ftp manager."""


from os import mkdir, path, walk
import json


from crawler.index.index import count_files_index
#from crawler.index.ftp_manager import SFTPManager as FTPManager
from crawler.index.ftp_manager import FTPManager
from crawler.swiftea_bot.data import DIR_INDEX
from crawler.swiftea_bot.module import tell


class FTPSwiftea(FTPManager):
	"""Class to manage the ftp connection for crawler."""
	def __init__(self, config):
		host = config['FTP_HOST']
		user = config['FTP_USER']
		password = config['FTP_PASSWORD']
		port = config['FTP_PORT']
		path_index = config['FTP_INDEX']
		path_data = config['FTP_DATA']

		FTPManager.__init__(self, host, user, password, port)
		self.path_index = path_index
		self.path_data = path_data

	def set_ftp_index(self, path_index):
		self.path_index = path_index

	def get_inverted_index(self):
		"""Get inverted-index.

		:return: inverted-index and True if an error occured

		"""
		tell('Get inverted-index from server')
		self.downuploaded_files = 0
		inverted_index = dict()
		self.connection()
		self.cd(self.path_index)
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
		self.connection()
		self.cd(self.path_index)

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

		:return: `server` if must download from server, `new` if there is no inverted index.

		"""
		self.connection()
		self.cd(self.path_index)
		if path.exists(DIR_INDEX):

			def get_size(start_path = '.'):
			    total_size = 0
			    for dirpath, dirnames, filenames in walk(start_path):
			        for f in filenames:
			            fp = path.join(dirpath, f)
			            total_size += path.getsize(fp)
			    return total_size

			local_size = get_size(DIR_INDEX)
			server_size = self.get_total_size()
			if local_size < server_size:
				response = 'server'
			else:
				response = 'local'
		elif 'FR' in self.listdir():
			response = 'server'
		else:
			response = 'new'

		self.disconnect()
		return response

	def download_lists_words(self):
		"""Download stopwords and badwords."""
		tell('download list of words')
		self.connection()
		for filename in ['en.stopwords.txt', 'fr.stopwords.txt', 'en.badwords.txt', 'fr.badwords.txt']:
			type_ = filename[3:-4] + '/'
			self.cd(self.path_data + type_)
			self.get(type_ + filename, filename)
		self.disconnect()

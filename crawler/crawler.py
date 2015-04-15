#!/usr/bin/python3

"""Crawler for Swiftea : http://swiftea.alwaysdata.net"""

from time import strftime


from package.module import speak, quit, start
from package.data import *
from package.private_data import *
from package.web_connexion import WebConnexion
from package.file_manager import FileManager
from package.database_swiftea import DatabaseSwiftea
from package.searches import SiteInformations
from package.inverted_index import InvertedIndex
from package.ftp_manager import FTPManager

__author__ = "Seva Nathan"

class Crawler:
	"""Crawler Class.

	response : a message
	result : data asked

	"""
	def __init__(self):
		self.site_informations = SiteInformations()
		if not self.site_informations.get_stopwords():
			quit()
		self.file_manager = FileManager()
		self.ftp_manager = FTPManager(HOST_FTP, USER, PASSWORD)
		self.index_manager = InvertedIndex()
		speak("Get index")
		self.inverted_index, to_read, response = self.ftp_manager.get_inverted_index()
		speak(response)
		if self.inverted_index == '0' and self.file_manager.reading_file_number != 0:
			speak("No index, quit program")
			quit()
		elif to_read != []:
			inverted_index = self.file_manager.get_inverted_index(to_read)
			for key in inverted_index.keys():
				self.inverted_index[key] = inverted_index[key]
		self.index_manager.setInvertedIndex(self.inverted_index)
		self.index_manager.setStopwords(self.site_informations.STOPWORDS)
		self.database = DatabaseSwiftea(HOST_DB, USER, PASSWORD, NAME_DB)
		self.web_connexion = WebConnexion()

		self.infos = list()
		self.crawled_websites = 0

	def start(self):
		speak(strftime("%d/%m/%y %H:%M:%S")) # speak time
		while True:
			for k in range(50):
				while len(self.infos) < 10:
					speak('Reading {0}, link {1}'.format(
						str(self.file_manager.reading_file_number),
						str(self.file_manager.reading_line_number+1)))
					# get the url of the website :
					url = self.file_manager.get_url()
					if url == 'stop':
						self.safe_quit()
					self.crawl_website(url)

				# end of crawling loop
				speak('{} new documents ! '.format(self.crawled_websites))

				self.send_to_db()
				self.indexing()
				
				# reset the list of dict of informations of websites :
				self.infos.clear()
				self.file_manager.check_stop_crawling()
				self.file_manager.get_max_links()
				self.file_manager.save_config()
				#self.file_manager.check_size_file()
				if self.file_manager.run == 'false':
					speak("User wants stop  program")
					self.safe_quit()

			# end of loop range(n)

			self.send_inverted_index()
			self.suggestions()

	def crawl_website(self, url):
		"""score : .5 encondig, .5 css, .5 language, """
		speak('Crawling url : ' + url)
		# get the webpage's html code :
		html_code, is_nofollow, score = self.web_connexion.get_code(url)
		if html_code is not None:
			if is_nofollow:
				url = url = url[:-10]
			webpage_infos = {}
			webpage_infos['url'] = url
			(links, webpage_infos['title'], webpage_infos['description'],
				webpage_infos['keywords'], webpage_infos['language'],
				webpage_infos['score'], webpage_infos['nb_words'],
				webpage_infos['favicon'],
				) = self.site_informations.get_infos(url, html_code, is_nofollow, score)

			if webpage_infos['title'] != '':
				self.infos.append(webpage_infos)
				self.crawled_websites += 1
				self.file_manager.save_links(links)

	def send_to_db(self):
		"""Send info to database."""
		response_url = self.database.send_infos(self.infos)
		if response_url:
			self.safe_quit()

	def indexing(self):
		for webpage_infos in self.infos:
			doc_id = self.database.get_doc_id(webpage_infos['url'])
			if doc_id == 'error':
				self.safe_quit()
			speak('Indexing : {0} {1}'.format(doc_id, webpage_infos['url']))
			self.inverted_index = self.index_manager.append_doc(webpage_infos['keywords'], doc_id)
			if self.inverted_index is None:
				self.database.del_one_doc(webpage_infos['url'], 'index_url')

	def send_inverted_index(self):
		speak('Send index')
		response = self.ftp_manager.send_inverted_index(self.index_manager.getInvertedIndex())
		if response:
			speak("Failed to send index : " + response, 21)
			self.safe_quit()
		else:
			speak('All transferts are completed')

	def suggestions(self):
		"""Suggestions :

		Get 5 urls from database, delete them, crawl them,
		send all infos of them, index them and return to main loop.

		"""
		suggestions = self.database.suggestions()
		if suggestions is not None:
			speak('Failed to get suggestions')
		else:
			suggestions = self.site_informations.clean_links(suggestions)
			if len(suggestions) > 0:
				speak('Suggestions : ')
			else:
				speak('No suggestions')
			for url in suggestions:
				self.crawl_website(url)
			self.send_to_db()
			self.indexing()
			self.infos.clear() # reset the list of dict of informations of websites :

	def safe_quit(self):
		self.send_inverted_index()
		speak('Programm will quit')
		quit()

if __name__ == '__main__':
	start()
	crawler = Crawler()
	crawler.start()

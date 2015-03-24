#!/usr/bin/python3

"""Crawler for Swiftea : http://swiftea.alwaysdata.net"""

from time import strftime


from package.module import speak, leaving, start
from package.data import *
from package.private_data import *
from package.web_connexion import WebConnexion
from package.file_management import FileManagement
from package.database_swiftea import DataBase_swiftea
from package.searches import SiteInformations
from package.inverted_index import InvertedIndex
from package.FTP_swiftea import FTPSwiftea

__author__ = "Seva Nathan"

class Crawler:
	"""Crawler Class.

	rep : a message
	result : data asked

	"""
	def __init__(self):
		start()
		self.web_site_infos = SiteInformations()
		if self.web_site_infos.get_back_stopwords() == 'error':
			leaving()
		self.file_management = FileManagement()
		self.ftp = FTPSwiftea(HOST_FTP, USER, PASSWORD)
		self.inverted_index = InvertedIndex()
		speak("Get index") # get back the index
		result, rep = self.ftp.get_index(FILE_INDEX, FTP_INDEX)
		if result is None and self.file_management.reading_file_number != 0:
			 # no index, program will stop :
			speak("No index, quit program")
			leaving()
		else:
			self.inverted_index.setIndex(result)
		self.inverted_index.setSTOP_WORDS(self.web_site_infos.STOP_WORDS)
		self.data_base = DataBase_swiftea(HOST_DB, USER, PASSWORD, NAME_DB)
		self.webconnexion = WebConnexion()

		self.infos = list()

	def start(self):
		nbr_page_crawl = 0
		speak(strftime("%d/%m/%y %H:%M:%S")) # speak time
		while True:
			for k in range(3):
				while len(self.infos) < 10:
					# speak what is happen : reading in file {}, link {}
					speak('Reading : {0}, links : {1}'.format(
						str(self.file_management.reading_file_number),
						str(self.file_management.reading_line_number+1)))
					# get the url of the web site :
					url = self.file_management.get_url()
					if url == 'stop':
						self.end() # quit program
					self.crawl_website(url)

					nbr_page_crawl += 1

				# end of crawling loop

				# {} new documents
				speak('{} new documents ! '.format(nbr_page_crawl))

				self.send_DB()
				self.indexation()
				# reset the list of dict of informations of web sites :
				self.infos.clear()
				# get_nbr_max, save_meters, get_stop, check_size_file :
				self.file_management.sometimes()
				# user wants stop ? :
				if self.file_management.run == 'false':
					speak("User wants stop  program")
					self.end()

			# end of loop range(3) : 30 web sites crawled

			self.send_index()
			self.suggestions()

	def crawl_website(self, url):
		"""score : .5 encondig, .5 css, .5 language, """
		speak('Crawled url : ' + url) # the  url is {}
		# get the code of webpage :
		code, nofollow, score = self.webconnexion.get_code(url)
		if code != 'continue':
			infoswebpage = {}
			infoswebpage['url'] = url
			(links, infoswebpage['title'], infoswebpage['description'],
				infoswebpage['keywords'], infoswebpage['language'],
				infoswebpage['score'], infoswebpage['nb_words'], infoswebpage['favicon']
				) = self.web_site_infos.start_job(url, code, nofollow, score)

			if infoswebpage['title'] != '':
				self.infos.append(infoswebpage)
				self.file_management.save_links(links)

	def send_DB(self):
		rep = self.data_base.send_infos(self.infos)
		if rep == 'error':
			self.end()

	def indexation(self):
		for infoswebpage in self.infos:
			id0 = self.data_base.get_id(infoswebpage['url'])
			if id0 == 'error':
				self.end()
			speak('Indexing : {0} {1}'.format( # indexing : id url
				str(id0[0]), infoswebpage['url']))
			rep = self.inverted_index.append_doc(infoswebpage, id0[0])
			if rep == 'del':
				self.data_base.del_one_doc(infoswebpage['url'], 'index_url')

	def send_index(self):
		rep = self.ftp.send_index(self.inverted_index.getIndex())
		if rep == 'error':
			self.end()

	def suggestions(self):
		"""Sugesstions

		Get back 5 urls from the data base
		Delete the 5 urls
		Crawl the 5 urls
		Send all the documents of the 5 urls
		Index the documents
		Tavk back the main loop

		"""
		speak('suggestions : ')
		suggestions = self.data_base.suggestions()
		if suggestions == 'error':
			# Can't get suggested urls
			speak('Failed to get suggestions')
			self.end() # ?
		else:
			suggestions = self.web_site_infos.clean_links(suggestions)
			for url in suggestions:
				self.crawl_website(url)
			self.send_DB()
			self.indexation()
			# reset the list of dict of informations of websites :
			self.infos.clear()

	def end(self):
		self.send_index()
		speak('Programm will quit')
		leaving()

if __name__ == '__main__':
	crawler = Crawler()
	crawler.start()
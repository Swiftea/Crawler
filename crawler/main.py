#!/usr/bin/python3

from time import strftime

try:
	import package.private_data as pvdata
except ImportError:
	pass
from package.module import speak, quit_program, create_dirs, is_index, create_doc, def_links
from package.web_connexion import WebConnexion
from package.file_manager import FileManager
from package.database_swiftea import DatabaseSwiftea
from package.searches import SiteInformations
from package.inverted_index import InvertedIndex
from package.ftp_swiftea import FTPSwiftea

class Crawler(object):
	"""Crawler main class."""
	def __init__(self):
		self.site_informations = SiteInformations()
		if self.site_informations.STOPWORDS is None:
			speak('No stopwords, quit program')
			quit_program()
		self.file_manager = FileManager()
		self.ftp_manager = FTPSwiftea(pvdata.HOST_FTP, pvdata.USER, pvdata.PASSWORD)
		self.get_inverted_index()
		self.index_manager = InvertedIndex()
		self.index_manager.setInvertedIndex(self.inverted_index)
		self.index_manager.setStopwords(self.site_informations.STOPWORDS)
		self.database = DatabaseSwiftea(pvdata.HOST_DB, pvdata.USER, pvdata.PASSWORD, pvdata.NAME_DB)
		self.web_connexion = WebConnexion()

		self.infos = list()
		self.crawled_websites = 0

	def get_inverted_index(self):
		"""Manage all operations to get inverted-index."""
		if is_index():
			self.inverted_index = self.file_manager.get_inverted_index()
		else:
			if self.ftp_manager.compare_indexs():
				self.inverted_index, error = self.ftp_manager.get_inverted_index()
			else:
				self.inverted_index = self.file_manager.read_inverted_index()
				error = False
			if error and self.file_manager.reading_file_number != 0:
				quit_program()

	def start(self):
		"""Start main loop of crawling."""
		speak(strftime("%d/%m/%y %H:%M:%S"))  # Speak time
		run = True
		while run:
			for _ in range(50):
				while len(self.infos) < 10:
					speak('Reading {0}, link {1}'.format(
						str(self.file_manager.reading_file_number),
						str(self.file_manager.reading_line_number+1)))
					# Get the url of the website :
					url = self.file_manager.get_url()
					if url == 'stop':
						self.safe_quit()
					self.crawl_webpage(url)

				# End of crawling loop

				speak('{} new documents ! '.format(self.crawled_websites))

				self.send_to_db()
				self.indexing()

				# Reset the list of dict of informations of websites :
				self.infos.clear()
				self.file_manager.check_stop_crawling()
				self.file_manager.get_max_links()
				self.file_manager.save_config()
				#self.file_manager.check_size_file()
				if self.file_manager.run == 'false':
					speak('User wants stop program')
					self.safe_quit()
					run = False
					break

			# End of loop range(n)
			if run:
				self.send_inverted_index()
				self.suggestions()

	def crawl_webpage(self, url):
		"""Crawl the given url.

		Webpage score is define here: 0.5 for giving encondig,
		0.5 for have css style file and 0.5 for specified language.

		:param url: url of webpage
		:type url: str
		"""
		speak('Crawling url : ' + url)
		# Get webpage's html code :
		html_code, is_nofollow, score = self.web_connexion.get_code(url)
		if html_code is None:
			speak('Ignore')
		elif html_code == 'no_connexion':
			self.file_manager.save_inverted_index(self.index_manager.getInvertedIndex())
			quit_program()
		else:
			if is_nofollow:
				url = url = url[:-10]
			webpage_infos = {}
			webpage_infos['url'] = url
			(links, webpage_infos['title'], webpage_infos['description'],
				webpage_infos['keywords'], webpage_infos['language'],
				webpage_infos['score'], webpage_infos['favicon'],
				) = self.site_informations.get_infos(url, html_code, is_nofollow, score)

			if webpage_infos['title'] != '':
				self.infos.append(webpage_infos)
				self.crawled_websites += 1
				self.file_manager.save_links(links)
			else:
				speak('Ignore')

	def send_to_db(self):
		"""Send all informations about crawled webpages to database."""
		response_url = self.database.send_infos(self.infos)
		if response_url:
			self.safe_quit()

	def indexing(self):
		"""Index crawled webpages."""
		for webpage_infos in self.infos:
			doc_id = self.database.get_doc_id(webpage_infos['url'])
			if doc_id is None:
				self.safe_quit()
			speak('Indexing : {0} {1}'.format(doc_id, webpage_infos['url']))
			timeout = self.index_manager.add_doc(webpage_infos['keywords'], doc_id, webpage_infos['language'])
			if timeout:
				self.database.del_one_doc(webpage_infos['url'], 'index_url')

	def send_inverted_index(self):
		"""Send inverted-index generate by indexing to ftp server."""
		error = self.ftp_manager.send_inverted_index(self.index_manager.getInvertedIndex())
		if error:
			self.file_manager.save_inverted_index(self.index_manager.getInvertedIndex())
			quit_program()

	def suggestions(self):
		"""Suggestions:

		Get 5 urls from database, delete them, crawl them,
		send all informations about them, index them and return to main loop.
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
			self.infos.clear()  # Reset the list of dict of informations of websites :

	def safe_quit(self):
		"""Send inverted-index and quit."""
		self.send_inverted_index()
		speak('Programm will quit')
		speak('end\n', 0)


if __name__ == '__main__':
	create_dirs()
	create_doc()
	def_links()
	crawler = Crawler()
	crawler.start()

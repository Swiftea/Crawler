#!/usr/bin/python3

from time import strftime

try:
	import package.private_data as pvdata
except ImportError:
	pass
from package.module import tell, quit_program, create_dirs, is_index, create_doc, def_links, dir_size, remove_duplicates
from package.data import DIR_INDEX
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
			tell('No stopwords, quit program')
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
		"""Manage all operations to get inverted-index.

		Check for a save inverted-index file, compare inverted-index in local and
		on server to know if it's necessary to download it.

		"""
		if is_index():
			self.inverted_index = self.file_manager.get_inverted_index()
		else:
			if self.ftp_manager.compare_indexs():
				self.inverted_index, error = self.ftp_manager.get_inverted_index()
			else:
				self.inverted_index = self.file_manager.read_inverted_index()
				error = False
			if error and self.file_manager.reading_file_number != 0:
				tell('Failed to download inverted-index ' + self.inverted_index, 1)
				quit_program()

	def start(self):
		"""Start main loop of crawling.

		Crawl 10 webpages, send documents to database, index them
		and save the configurations (line number in links file, ...).
		Send the inverted-index and check for suggestions each 500 crawled webpages.

		Do it until the user want stop crawling, occured an error, or fill the server.

		"""
		run = True
		while run:
			for _ in range(50):
				tell('Crawl', severity=2)
				while len(self.infos) < 10:
					tell('Reading {0}, link {1}'.format(
						str(self.file_manager.reading_file_number),
						str(self.file_manager.reading_line_number+1)), severity=0)
					# Get the url of the website :
					url = self.file_manager.get_url()
					if url == 'stop':
						self.safe_quit()
					self.crawl_webpage(url)
					# Remove duplicates:
					self.infos = remove_duplicates(self.infos)

				# End of crawling loop

				tell('{} new documents ! '.format(self.crawled_websites), severity=-1)

				self.send_to_db()
				self.indexing()

				self.infos.clear()  # Reset the list of dict of informations of websites.
				self.file_manager.check_stop_crawling()
				self.file_manager.get_max_links()
				self.file_manager.save_config()
				#self.file_manager.check_size_file()
				if self.file_manager.run == 'false':
					tell('User wants stop program')
					self.safe_quit()
					run = False
					break

			# End of loop range(n)
			if run:
				self.suggestions()
				self.send_inverted_index()
				if dir_size(DIR_INDEX) > 7000000:
					tell('Index is too big for current server', severity=-1)
					self.safe_quit()
					run = False

	def crawl_webpage(self, url):
		"""Crawl the given url.

		Get webpage source code, feed it to the parser, manager extracting data,
		manager redirections and can delete some documents to avoid duplicates.

		:param url: url of webpage
		:type url: str

		"""
		tell('Crawling ' + url)
		# Get webpage's html code:
		html_code, nofollow, score, new_url = self.web_connexion.get_code(url)
		if html_code is None:
			self.delete_if_exists(url)  # Failed to get code, must delete from database.
		elif html_code == 'no connexion':
			self.file_manager.save_inverted_index(self.index_manager.getInvertedIndex())
			quit_program()
		elif html_code == 'ignore':  # There was something wrong and maybe a redirection.
			self.delete_if_exists(url)
			if new_url:
				if url != new_url:
					self.delete_if_exists(new_url)
			else:
				tell('Bad redirection', severity=0)
		else:
			if url != new_url:
				tell('Redirect to ' + new_url, severity=0)
				self.delete_if_exists(url)
			webpage_infos = {}
			webpage_infos['url'] = new_url
			(links, webpage_infos['title'], webpage_infos['description'],
				webpage_infos['keywords'], webpage_infos['language'],
				webpage_infos['score'], webpage_infos['favicon'], webpage_infos['homepage']
				) = self.site_informations.get_infos(new_url, html_code, nofollow, score)

			if webpage_infos['title'] != '':
				self.infos.append(webpage_infos)
				self.crawled_websites += 1
				self.file_manager.save_links(links)
			else:
				self.delete_if_exists(new_url)

	def delete_if_exists(self, url):
		"""Delete bad doc if exists.

		Check if doc exists in database and delete it from database and inverted-index.

		:param url: url to delete
		:type url: str

		"""
		doc_exists = self.database.doc_exists(url)
		if doc_exists:
			doc_id = self.database.get_doc_id(url)
			if doc_id:
				self.database.del_one_doc(url)
				self.index_manager.delete_doc_id(doc_id)
			else:
				self.safe_quit()
		elif doc_exists is None:
			self.safe_quit()
		else:
			tell('Ignore: ' + url, severity=-1)

	def send_to_db(self):
		"""Send all informations about crawled webpages to database.

		Can delete some documents to avoid http and https duplicates.

		"""
		tell('Send to database', severity=2)
		for webpage_infos in self.infos:
			url_to_add, url_to_del = self.database.https_duplicate(webpage_infos['url'])
			webpage_infos['url'] = url_to_add
			if url_to_del:
				self.delete_if_exists(url_to_del)
			tell('New url: ' + webpage_infos['url'], severity=-1)
			error = self.database.send_doc(webpage_infos)
			if error:
				self.safe_quit()

	def indexing(self):
		"""Index crawled webpages.

		get id of each documents and index them.

		"""
		tell('Indexing', severity=2)
		for webpage_infos in self.infos:
			doc_id = self.database.get_doc_id(webpage_infos['url'])
			if doc_id is None:
				self.safe_quit()
			tell('Indexing {0} {1}'.format(doc_id, webpage_infos['url']))
			self.index_manager.add_doc(webpage_infos['keywords'], doc_id, webpage_infos['language'])

	def send_inverted_index(self):
		"""Send inverted-index generate by indexing to ftp server."""
		error = self.ftp_manager.send_inverted_index(self.index_manager.getInvertedIndex())
		if error:
			tell('Failed to send inverted-index ' + error, 2)
			self.file_manager.save_inverted_index(self.index_manager.getInvertedIndex())
			quit_program()

	def suggestions(self):
		"""Suggestions:

		Get 5 urls from database, delete them, crawl them,
		send all informations about them, index them and return to main loop.

		"""
		suggestions = self.database.suggestions()
		if suggestions is not None:
			tell('Failed to get suggestions')
		else:
			suggestions = self.site_informations.clean_links(suggestions)
			if len(suggestions) > 0:
				tell('Suggestions', severity=2)
			else:
				tell('No suggestions', severity=0)
			for url in suggestions:
				self.crawl_website(url)
			self.send_to_db()
			self.indexing()
			self.infos.clear()  # Reset the list of dict of informations of websites.

	def safe_quit(self):
		"""Save inverted-index and quit."""
		self.file_manager.save_inverted_index(self.index_manager.getInvertedIndex())
		tell('Programm will quit', severity=2)
		tell('end\n', 0, 0)


if __name__ == '__main__':
	create_dirs()
	create_doc()
	def_links()
	crawler = Crawler()
	crawler.start()

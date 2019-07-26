#!/usr/bin/env python3

from time import time
from os import path


try:
	import swiftea_bot.private_data as pvdata
except ImportError:
	pass

from swiftea_bot import data, module, links
from crawler import Crawler
from swiftea_bot.file_manager import FileManager


class CrawlerDomain(Crawler):
	"""Crawler main class."""
	def __init__(self, crawl_option, url):
		Crawler.__init__(self);
		print(crawl_option)
		self.file_manager = FileManager(crawl_option)
		self.crawl_option = crawl_option
		# self.crawl_option['level'] = links.get_level(crawl_option['domain'])
		if not path.exists(data.FILE_LINKS):
			links.save_domains([{
				'domain': crawl_option['domain'],
				'level': self.crawl_option['level'],
				'completed': False,
				'line': 0
			}])
		self.file_manager.save_links([url])

	def start(self):
		"""Start main loop of crawling.

		Crawl 10 webpages, send documents to database, index them
		and save the configurations (line number in links file, ...).
		Send the inverted-index and check for suggestions each 500 crawled webpages.

		Do it until the user want stop crawling or occured an error.

		"""
		print('Starting with', self.crawl_option)
		# input('Go?')
		if (self.crawl_option['target-level'] <= self.crawl_option['level']):
			print('Already done')
			return
		run = True
		while run:
			stats_send_index = time()
			begining = time()

			url, level_complete = self.file_manager.get_url()
			if url == 'error':
				module.safe_quit()
			elif url == '#target-reached#':
				module.tell('Target level reached')
				break

			result = self.crawl_webpage(url)
			# result[0]: webpage_infos, result[1]: links

			if result:
				self.infos.append(result[0])
				# save links and get next url:
				self.file_manager.save_links(result[1])

			with open(data.DIR_STATS + 'stat_crawl_one_webpage', 'a') as myfile:
				myfile.write(str(time() - begining) + '\n')

			# End of crawling loop

			module.tell(
				'{} new documents!'.format(self.crawled_websites),
				severity=-1
			)

			self.send_to_db()
			self.indexing()

			self.infos.clear()  # Reset the list of dict of informations of websites.
			self.file_manager.check_stop_crawling()
			self.file_manager.save_config()
			if self.file_manager.run == 'false':
				module.tell('User wants stop program')
				module.safe_quit()

			if self.crawl_option['level'] == self.crawl_option['target-level'] + 1:
				run = False
				break

			self.send_inverted_index()
			self.file_manager.check_size_files()
			module.stats_send_index(stats_send_index, time())
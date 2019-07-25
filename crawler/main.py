#!/usr/bin/env python3

import atexit
from urllib.parse import urlparse


import click


from swiftea_bot import module
from crawler import Crawler
from crawler_domain import CrawlerDomain


def save(crawler):
	crawler.file_manager.save_inverted_index(
		crawler.index_manager.get_inverted_index()
	)

@click.command()
@click.option('-u', '--url')  # initial url
@click.option('-sd', '--sub-domain', default=True)  # True or False
@click.option('-l', '--level', default=1)
def main(url, sub_domain, level):
	# python main.py -u http://idesys.org -sd False -l 2
	# python main.py -u http://idesys.org -l 1
	crawl_option = {'domain': '', 'level': -1}
	module.create_dirs()
	if url:
		crawler = CrawlerDomain(crawl_option)
		crawl_option['domain'] = urlparse(url).netloc
		crawl_option['sub-domain'] = sub_domain
		crawl_option['target-level'] = level
		crawl_option['level'] = swiftea_bot.links.get_level(crawl_option['domain'])
		print('Starting with', crawl_option)
		# input('Go?')
		if (crawl_option['target-level'] <= crawl_option['level']):
			print('Already done')
			return
	else:
		crawler = Crawler()
		print('Starting with base urls')
		module.def_links()
	atexit.register(save, crawler)
	crawler.start()


if __name__ == '__main__':
	main()

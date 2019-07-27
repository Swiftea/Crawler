#!/usr/bin/env python3

# import atexit
from urllib.parse import urlparse


import click


from swiftea_bot import module
from crawler import Crawler
from crawler_domain import CrawlerDomain



@click.command()
@click.option('-u', '--url')  # initial url
@click.option('-sd', '--sub-domain', default=True)  # True or False
@click.option('-l', '--level', default=0)
@click.option('-tl', '--target-level', default=1)
# def save(crawler):
# 	crawler.file_manager.save_inverted_index(
# 		crawler.index_manager.get_inverted_index()
# 	)

def main(url='http://idesys.org', sub_domain=False, level=0, target_level=1):
	# python main.py -u http://idesys.org -sd False -l 2
	# python main.py -u http://idesys.org -l 1
	module.create_dirs()
	if url:
		crawl_option = dict()
		crawl_option['domain'] = urlparse(url).netloc
		crawl_option['sub-domain'] = sub_domain
		crawl_option['level'] = level
		crawl_option['target-level'] = target_level
		crawler = CrawlerDomain(crawl_option, url)
	else:
		crawler = Crawler()
		print('Starting with base urls')
		module.def_links()
	# atexit.register(save, crawler)
	crawler.start()


if __name__ == '__main__':
	main()

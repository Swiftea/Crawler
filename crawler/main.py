#!/usr/bin/env python3

import atexit
from urllib.parse import urlparse
import json
import os
import sys


from crawler.swiftea_bot import module
from crawler.crawler_base import Crawler
from crawler.crawler_domain import CrawlerDomain


def save(crawler):
	crawler.file_manager.save_inverted_index(
		crawler.index_manager.get_inverted_index()
	)
	os.chdir('..')

def main(url='', sub_domain=True, level=0, target_level=1, use_mongodb=False, loop_1=50, loop_2=10, dir_data=''):
	with open('crawler-config.json') as json_file:
		config = json.load(json_file)
	if dir_data != '':
		config['DIR_DATA'] = dir_data
	if not os.path.isdir(config['DIR_DATA']):
		os.mkdir(config['DIR_DATA'])
	os.chdir(config['DIR_DATA'])
	module.create_dirs()
	if url:
		crawl_option = dict()
		crawl_option['domain'] = urlparse(url).netloc
		crawl_option['sub-domain'] = sub_domain
		crawl_option['level'] = level
		crawl_option['target-level'] = target_level
		crawl_option['use-mongodb'] = use_mongodb
		crawler = CrawlerDomain(config, crawl_option, url)
	else:
		print('Starting with base urls')
		crawler = Crawler(config, loop_1, loop_2)
		module.def_links()
		atexit.register(save, crawler)
	crawler.start()

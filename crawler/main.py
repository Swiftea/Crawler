#!/usr/bin/env python3

import atexit
from urllib.parse import urlparse
import json
import os
import sys


from crawler.swiftea_bot import module
from crawler.crawler_base import Crawler
from crawler.crawler_domain import CrawlerDomain


def main(url='', sub_domain=True, level=0, target_level=1, use_mongodb=False, l1=50, l2=10, dir_data=''):
	with open('crawler-config.json') as json_file:
		config = json.load(json_file)
	if dir_data != '':
		config['DIR_DATA'] = dir_data
	if not os.path.isdir(config['DIR_DATA']):
		os.mkdir(config['DIR_DATA'])
	os.chdir(config['DIR_DATA'])
	module.create_dirs(config['DIR_INDEX'])
	if url:
		crawl_option = dict()
		crawl_option['domain'] = urlparse(url).netloc
		crawl_option['sub-domain'] = sub_domain
		crawl_option['level'] = level
		crawl_option['target-level'] = target_level
		crawl_option['use-mongodb'] = use_mongodb
		crawler = CrawlerDomain(config, crawl_option, url)
	else:
		crawler = Crawler(config, l1, l2)
		module.def_links()
		atexit.register(module.quit, crawler)
	return crawler

# if __name__ == '__main__':
# 	crawler = main()
# 	try:
# 		crawler.start()
# 	except KeyboardInterrupt:
# 		module.quit(crawler)

#!/usr/bin/env python3


import crawler.stats
import crawler.main
import crawler.crawler_base
import crawler.crawler_domain
from crawler.swiftea_bot.data import DIR_STATS

def test_stats():
	crawler.stats.stats()

def test_compress_stats():
	crawler.stats.compress_stats(DIR_STATS + 'stat_webpages')

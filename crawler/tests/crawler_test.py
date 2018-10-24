#!/usr/bin/env python3


import stats
from swiftea_bot.data import DIR_STATS

def test_stats():
	stats.stats()

def test_compress_stats():
	stats.compress_stats(DIR_STATS + 'stat_webpages')

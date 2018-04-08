#!/usr/bin/env python3

import sys


import stats
import main
from swiftea_bot.data import DIR_STATS


class CrawlerBaseTest(object):
	def setup_method(self, _):
		self.defstdout = sys.__stdout__


class TestStats(CrawlerBaseTest):
	def test_stats(self):
		stats.stats()

	def test_compress_stats(self):
		stats.compress_stats(DIR_STATS + 'stat_webpages')

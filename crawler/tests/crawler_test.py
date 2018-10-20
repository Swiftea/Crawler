#!/usr/bin/env python3

import sys


import stats
import main
from swiftea_bot.data import DIR_STATS

class TestStats:
	def test_stats(self):
		stats.stats()

	def test_compress_stats(self):
		stats.compress_stats(DIR_STATS + 'stat_webpages')

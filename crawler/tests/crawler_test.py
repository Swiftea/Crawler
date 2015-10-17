#!/usr/bin/python3

import sys

import stats
import main
from swiftea_bot.data import DIR_STATS
from tests.global_test import RedirectOutput

class CrawlerBaseTest(object):
	def setup_method(self, _):
		self.defstdout = sys.__stdout__


class TestGlobalTest(CrawlerBaseTest):
	def test_RedirectOutput(self):
		sys.stdout = RedirectOutput('test_RedirectOutput.ext')
		print('A test message')


class TestStats(CrawlerBaseTest):
	def test_stats(self):
		stats.stats()

	def test_compress_stats(self):
		stats.compress_stats(DIR_STATS + 'stat_webpages')

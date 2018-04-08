#!/usr/bin/python3

"""How to:

With coverage report (same way than travis):
    export PYTHONPATH=crawler
    coverage run setup.py test
    coverage report
    coverage html

"""

from sys import argv
import os

import pytest

try:
    from crawler.tests.test_data import reset
except ImportError:
    from tests.test_data import reset


def run_tests(local=False):
    os.chdir('crawler/tests')
    args = ['--strict', '--verbose']
    args.append('swiftea_bot_test.py')
    args.append('crawling_test.py')
    args.append('database_test.py')
    args.append('index_test.py')
    if local:
        args.append('crawler_test.py')
        args.append('global_test.py')
    errno = pytest.main(args)
    reset()
    return errno


if __name__ == '__main__':
    run_tests(True)

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

from crawler.tests.test_data import reset

def run_tests():
    os.chdir('crawler/tests')
    args = ['--strict', '--verbose']
    args.append('swiftea_bot_test.py')
    args.append('crawling_test.py')
    args.append('database_test.py')
    args.append('index_test.py')
    args.append('crawler_test.py')
    errno = pytest.main(args)
    reset()
    return errno

def tests(args=['--strict', '--verbose']):
    if 'file' not in args:
        if __name__ == '__main__':
            args.append(path + 'global_test.py ')
        args.append(path + 'swiftea_bot_test.py ')
        args.append(path + 'crawling_test.py ')
        args.append(path + 'database_test.py ')
        args.append(path + 'index_test.py ')
        args.append(path + 'crawler_test.py ')
    errno = pytest.main(args)
    reset()
    return errno

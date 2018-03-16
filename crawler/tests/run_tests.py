#!/usr/bin/python3

"""How to:

With coverage report (same way than travis):
    export PYTHONPATH=crawler
    coverage run setup.py test
    coverage report
    coverage html

"""

import pytest
from sys import argv

def run_tests():
    from crawler.tests.test_data import reset
    path = 'crawler/tests/'
    args = ['--strict', '--verbose']
    args.append(path + 'swiftea_bot_test.py')
    args.append(path + 'crawling_test.py')
    args.append(path + 'database_test.py')
    args.append(path + 'index_test.py')
    args.append(path + 'crawler_test.py')
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

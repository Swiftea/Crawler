#!/usr/bin/env python3

"""How to:

With coverage report (same way than travis):
    export PYTHONPATH=crawler
    coverage run setup.py test
    coverage report
    coverage html

"""

import pytest


from crawler.tests.test_data import reset

def run_tests(local=False):
    args = ['--strict', '--verbose', '-vv']
    args.append('crawler/tests/swiftea_bot_test.py')
    args.append('crawler/tests/crawling_test.py')
    args.append('crawler/tests/database_test.py')
    args.append('crawler/tests/index_test.py')
    args.append('crawler/tests/crawler_test.py')
    if local:
        args.append('crawler/tests/crawler_test.py')
        args.append(crawler/tests/'global_test.py')
    print('Warning: data folder will be overwrite')
    errno = pytest.main(args)
    reset()
    return errno


if __name__ == '__main__':
    run_tests(True)

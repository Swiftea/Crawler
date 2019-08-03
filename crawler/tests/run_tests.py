#!/usr/bin/env python3

"""How to:

With coverage report (same way than travis):
    export PYTHONPATH=crawler
    coverage run setup.py test
    coverage report
    coverage html

"""


# import os


import pytest


from crawler.tests.test_data import reset


def run_tests(local=False, DIR_DATA='data_test'):
    # if not os.path.exists(DIR_DATA):
    #     os.mkdir(DIR_DATA)
    # os.chdir(DIR_DATA)
    args = ['--strict', '--verbose', '-vv']
    args.append('crawler/tests/swiftea_bot_test.py')
    args.append('crawler/tests/crawling_test.py')
    args.append('crawler/tests/database_test.py')
    args.append('crawler/tests/index_test.py')
    args.append('crawler/tests/crawler_test.py')
    if local:
        args.append('crawler/tests/crawler_test.py')
        args.append(crawler/tests/'global_test.py')
    errno = pytest.main(args)
    reset(DIR_DATA)
    return errno


if __name__ == '__main__':
    run_tests(True)

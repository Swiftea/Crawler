#!/usr/bin/python3

import pytest
from sys import argv

try:
    from test_data import reset
except ImportError:
    from crawler.tests.test_data import reset

global path
global args
path = 'crawler/tests/'
args = '--strict --verbose'

def tests():
    tests = str()
    if __name__ == '__main__':
        tests += 'global_test.py '
    tests += path + 'swiftea_bot_test.py '
    tests += path + 'crawling_test.py '
    tests += path + 'database_test.py '
    tests += path + 'index_test.py '
    tests += args
    errno = pytest.main(tests)
    reset()
    return errno

if __name__ == '__main__':
    path = ''
    args = list()
    for arg in argv:
        args.append(arg)
    args = ' '.join(args[1:])  # Remove filename from tests args
    errno = tests()
    print('Tests exited with ' + str(errno))

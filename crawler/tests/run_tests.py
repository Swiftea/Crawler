#!/usr/bin/python3

"""How to:

With coverage report (same way than travis):
    export PYTHONPATH=crawler
    coverage run setup.py test
    coverage report
    coverage html

In command line:
    cd crawler/tests
    python run_tests.py [args for pytest]
    python run_tests.py file [testfilename] [args for pytest]  # Test given file.

    py.test [filetest]

Unit testing:
    cd crawler/tests
    import crawling_test as t
    test_class = t.TestWebConnexion
    test_class.setup_method(None)
    test_class.test_check_robots_perm()

"""

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

def tests(args='--strict --verbose'):
    tests = str()
    if 'file' not in args:
        if __name__ == '__main__':
            tests += 'global_test.py '
        tests += path + 'swiftea_bot_test.py '
        tests += path + 'crawling_test.py '
        tests += path + 'database_test.py '
        tests += path + 'index_test.py '
        tests += path + 'crawler_test.py '
    else:
        args = args[5:]
    tests += args
    errno = pytest.main(tests)
    reset()
    return errno

if __name__ == '__main__':
    path = ''
    args = list()
    for arg in argv:
        args.append(arg)
    args = ' '.join(args[1:])
    errno = tests(args)
    print('Tests exited with ' + str(errno))

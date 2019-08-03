#!/usr/bin/env python3

import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        from crawler.tests.run_tests import run_tests
        errno = run_tests()
        sys.exit(errno)

def read(filename):
    with open(filename, 'r') as myfile:
        return myfile.read()

setup(
    name = "swiftea-crawler",
    version = "1.1.2",
    author = "Thykof",
    author_email="thykof@protonmail.ch",
    tests_require=['pytest'],
    install_requires=read('requirements.txt').split(),
    cmdclass={'test': PyTest},
    description = ("Swiftea's Open Source Web Crawler"),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    license = "GNU GPL v3",
    keywords = "crawler swiftea",
    url = "https://github.com/Swiftea/Crawler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3'
    ],
    extras_require={
        'testing': ['pytest', 'coverage']
    }
)

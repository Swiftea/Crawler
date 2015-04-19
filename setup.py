import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'crawler/tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name = "Crawler",
    version = "0.1",
    author = "Thykof",
    tests_require=['pytest'],
    install_requires=['reppy>=0.3.0',
                    'PyMySQL>=0.6.6',
                    'urllib3>=1.10.2'
                    ],
    cmdclass={'test': PyTest},
    description = ("Swiftea's Open Source Web Crawler"),
    license = "GNU GPL v3",
    keywords = "crawler swiftea",
    url = "https://github.com/Swiftea/Crawler",
    packages=['crawler'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        'Operating System :: OS Independent',
    ],
    extras_require={
        'testing': ['pytest']
    }
)

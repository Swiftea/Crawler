import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description. It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Crawler",
    version = "0.1",
    author = "Thykof",
    tests_require=['pytest'],
    install_requires=['reppy>=0.3.0',
                    'PyMySQL>=0.6.6',
                    'urllib3>=1.10.1'
                    ],
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

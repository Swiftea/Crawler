# Swiftea's Open Source Web Crawler

## Master branch :
[![Build Status](https://travis-ci.org/Swiftea/Swiftea-Crawler.svg?branch=master)](https://travis-ci.org/Swiftea/Swiftea-Crawler)
[![Coverage Status](https://coveralls.io/repos/Swiftea/Swiftea-Crawler/badge.svg?branch=master)](https://coveralls.io/r/Swiftea/Swiftea-Crawler?branch=master)
[![Documentation Status](https://readthedocs.org/projects/crawler/badge/?version=master)](https://crawler.readthedocs.org/en/master/)
[![Code Health](https://landscape.io/github/Swiftea/Swiftea-Crawler/master/landscape.svg?style=flat)](https://landscape.io/github/Swiftea/Swiftea-Crawler/master)

## Develop branch :
[![Build Status](https://travis-ci.org/Swiftea/Swiftea-Crawler.svg?branch=develop)](https://travis-ci.org/Swiftea/Swiftea-Crawler)
[![Coverage Status](https://coveralls.io/repos/Swiftea/Swiftea-Crawler/badge.svg?branch=develop)](https://coveralls.io/r/Swiftea/Swiftea-Crawler?branch=develop)
[![Documentation Status](https://readthedocs.org/projects/crawler/badge/?version=develop)](https://crawler.readthedocs.org/en/develop)
[![Code Health](https://landscape.io/github/Swiftea/Swiftea-Crawler/develop/landscape.svg?style=flat)](https://landscape.io/github/Swiftea/Swiftea-Crawler/develop)

## Description

Swiftea's Crawler is the crawler we used on Swiftea. Currently, it can :

  - Visit websites
    - check robots.txt
    - search encoding
  - Parse them
    - extract data
        - title
        - description
        - ...
    - extract important words
        - filter stopwords
  - Index them
    - in database
    - in inverted-index

## Tech

Swiftea's Crawler uses a number of open source projects to work properly:

* [Python 3]

## Contributing

Want to contribute? Great!

Fork the repository. Then, run:

    git clone --recursive git@github.com:<username>/Swiftea-Crawler.git
    cd Swiftea-Crawler
    git flow init -d
    git flow feature start <your feature>

Then, do work and commit your changes. Finally publish your feature.

    git flow feature publish <your feature>

When done, open a pull request to your feature branch.

### Commit conventions :

#### General
  - Use the present tense
  - Use the imperative mood

#### Examples
  - Add something : "Add feature ..."
  - Update : "Update ..."
  - Improve something : "Improve ..."
  - Change something : "Change ..."
  - Fix something : "Fix ..."
  - Fix an issue : "Fix #123456" or "Close #123456"

License
----

GNU GENERAL PUBLIC LICENSE (v3)

**Free Software, Hell Yeah!**

[Python 3]:https://www.python.org/

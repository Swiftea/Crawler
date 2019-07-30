# Swiftea Crawler

[![Build Status](https://travis-ci.org/Swiftea/Crawler.svg?branch=master)](https://travis-ci.org/Swiftea/Crawler)
[![Coverage Status](https://coveralls.io/repos/github/Swiftea/Crawler/badge.svg?branch=master)](https://coveralls.io/github/Swiftea/Crawler?branch=master)
[![Documentation Status](https://readthedocs.org/projects/crawler/badge/?version=master)](http://crawler.readthedocs.io/en/master/?badge=master)
[![Code Health](https://landscape.io/github/Swiftea/Crawler/master/landscape.svg?style=flat)](https://landscape.io/github/Swiftea/Crawler/master)
[![Requirements Status](https://requires.io/github/Swiftea/Crawler/requirements.svg?branch=master)](https://requires.io/github/Swiftea/Crawler/requirements/?branch=master)

## Description

Swiftea-Crawler is an open source web crawler for Swiftea search engine.

Currently, it can:
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
  - Archive log files in a zip file

## Install and usage

### Setup

    virtualenv -p /usr/bin/python3 crawler-env
    source crawler-env/bin/activate
    pip install -r requirements.txt
    export PYTHONPATH=crawler

If the files below don't exist, the crawler will download them from our server:

- data/stopwords/fr.stopwords.txt
- data/stopwords/en.stopwords.txt
- data/badwords/fr.badwords.txt
- data/badwords/en.badwords.txt

### Run tests

Using only pytest:

    python setup.py test

With coverage:

    coverage run setup.py test
    coverage report
    coverage html

### Run crawler

    python crawler/main.py

### Build documentation

You must install `python3-sphinx` package.

    cd docs
    make html

## Deploy

Create directories in ftp server:

 - /www/data/badwords
 - /www/data/stopwords
 - /www/data/inverted_index

Upload the list of words: `/www/[type]/[lang].[type].txt`.

Create database with `sql/swiftea_mysql_db.sql`.

Create `crawler/swiftea_bot/private_data.py` with the folowing env variables:

		DB_HOST
		DB_USER
		DB_PASSWORD
		DB_NAME
		TABLE_NAMES = ['website', 'suggestion']
		FTP_HOST
		FTP_USER
		FTP_PASSWORD
		FTP_PORT
		FTP_DATA
		FTP_INDEX
		HOST

## How it works?

### Database:
The DatabaseSwiftea object can:
 - send documents
 - get the id of a document by the url
 - delete a document
 - select the suggestions
 - check if a doc exists
 - check for http and https duplicate

## Limits

When stoping the crawler (ctrl+V), it will not restart with the interupted url.

There are some little bugs with in the file `data/links/links.json`: some items are missing the `file` value.

## Version

Current version is 1.0.2

## Tech

Swiftea's Crawler uses a number of open source projects to work properly:

- [Python 3](https://www.python.org/)
  - [Reppy](https://github.com/seomoz/reppy)
  - [PyMySQL](https://github.com/PyMySQL/PyMySQL/)
  - [Requests](https://github.com/kennethreitz/requests)


## Contributing

Want to contribute? Great!

Fork the repository. Then, run:

    git clone git@github.com:<username>/Crawler.git
    cd Crawler

Then, do your work and commit your changes. Finally, make a pull request.

### Commit conventions:

#### General
  - Use the present tense
  - Use the imperative mood

#### Examples
  - Add something: "Add feature ..."
  - Update: "Update ..."
  - Improve something: "Improve ..."
  - Change something: "Change ..."
  - Fix something: "Fix ..."
  - Fix an issue: "Fix #123456" or "Close #123456"

License
----

GNU GENERAL PUBLIC LICENSE (v3)

**Free Software, Hell Yeah!**

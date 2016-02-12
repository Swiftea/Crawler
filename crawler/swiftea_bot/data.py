#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Define required data for crawler."""

from socket import setdefaulttimeout

from datetime import timedelta

setdefaulttimeout(30)

# Strings for directories and files:
DIR_DATA = 'data/'
DIR_LINKS = DIR_DATA + 'links/'
DIR_CONFIG = DIR_DATA + 'config/'
DIR_OUTPUT = DIR_DATA + 'output/'
DIR_INDEX = DIR_DATA + 'inverted_index/'
DIR_STATS = DIR_DATA + 'stats/'
FILE_EVENTS = DIR_CONFIG + 'events.log'
FILE_ERRORS = DIR_CONFIG + 'errors.log'
FILE_CONFIG = DIR_CONFIG + 'config.ini'
FILE_DOC = DIR_CONFIG + 'Readme'
FILE_BASELINKS = DIR_LINKS + '0'
FILE_INDEX = DIR_DATA + 'inverted_index.json'

# String for server:
SFTP_INDEX = 'html/data/inverted_index'
HOST = 'https://swiftea.ovh'

# Lists for clean up links and keywords:
BAD_EXTENTIONS = ('.pdf', '.doc', '.xls', '.zip', '.png', '.jpg', '.jpeg', '.bmp', '.gif',
'.ico', '.svg', '.tiff', '.tif' '.raw', '.flv', '.mpeg', '.mpg', '.wma', '.mp4', '.mp3', '.fla', '.avi', '.gz', '.exe', '.xml')
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
LIST_TAG_WORDS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'th', 'td']
LIST_ALONE_TAG_WORDS = ['a']

# Others informations:
USER_AGENT = 'Swiftea-Bot'
HEADERS = {"User-Agent": USER_AGENT}
MAX_LINKS = 5000  # Max links in a file
MAX_SIZE = 5000  # Max lines in events.log and errors.log
CRAWL_DELAY = timedelta(days=2)  # Program don't crawl the same website after this delay
TIMEOUT = 30
LANGUAGES = ['fr', 'en']

BASE_LINKS = """http://www.planet-libre.org
https://zestedesavoir.com
http://www.01net.com
https://www.youtube.com
http://www.lefigaro.fr
http://www.lemonde.fr
http://www.lepoint.fr
http://www.sport.fr
http://www.jeuxvideo.com
http://www.rueducommerce.fr
http://www.actu-environnement.com
https://fr.wikipedia.org
https://fr.news.yahoo.com
http://www.live.com
http://www.yahoo.com
http://www.lequipe.fr
http://trukastuss.over-blog.com
""" + HOST

#!/usr/bin/python3

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
FILE_NEWS = DIR_CONFIG + 'events.log'
FILE_ERROR = DIR_CONFIG + 'errors.log'
FILE_CONFIG = DIR_CONFIG + 'config.ini'
FILE_DOC = DIR_CONFIG + 'Readme'
FILE_BASELINKS = DIR_LINKS + '0'
FILE_INDEX = DIR_DATA + 'inverted_index.json'
FILE_DOCS = DIR_DATA + 'docs.json'

# String for server:
FTP_INDEX = '/var/www/html/data/inverted_index'
HOST = 'http://vps193469.ovh.net/'

# Lists for clean up links and keywords:
BAD_EXTENTIONS = ('.pdf', '.doc', '.xls', '.zip', '.png', '.jpg', '.jpeg', '.bmp', '.gif',
'.ico', '.svg', '.tiff', '.tif' '.raw', '.flv', '.mpeg', '.mpg', '.wma', '.mp4', '.mp3', '.fla', '.avi', '.gz', '.exe', '.xml')
START_CHARS = ('«', '\'', '"', '(', ':', '/' , '[', '{', '-', '“')
END_CHARS = ('.', ',', ';', '!', '?', '»', '\'', '"', ')', ':', '/', ']', '}', '-', '”', '…')
MIDLE_CHARS = '’'
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# Others informations:
USER_AGENT = 'Swiftea-Bot'
HEADERS = {"User-Agent": USER_AGENT}
MAX_LINKS = 5000  # Max links in a file
CRAWL_DELAY = timedelta(days=2)  # Program don't crawl the same website after this delay
TIMEOUT = 30
LANGUAGES = ['fr', 'en']

ERROR_CODE_DOC = """Error codes
===========

0: End,

1: Failed to download inverted-index
2: Failed to send inverted-index

3: Connexion to webpage failed: read timeout error (urllib3)
4: website not respoding
5: Connexion to webpage failed
6: Error robots.txt (reppy)
7: Error robots.txt (timeout)
8: Error robots.txt (requests)

9: Failed to update row in database
10: Failed to add row in database
11: Failed to get id in database
12: Doc not removed in database
13: Failed to get url in database
14: Failed to check row
"""

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
http://swiftea.alwaysdata.net
http://trukastuss.over-blog.com"""

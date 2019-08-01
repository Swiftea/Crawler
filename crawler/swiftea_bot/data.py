#!/usr/bin/env python3

"""Define required data by crawler."""


from socket import setdefaulttimeout
from datetime import timedelta


# Needed by Travis
try:
    from crawler.swiftea_bot.private_data import HOST
except ImportError:
    HOST = ''


setdefaulttimeout(30)

# Strings for directories and files:
DIR_LINKS = 'links/'
FILE_LINKS = DIR_LINKS + 'links.json'
DIR_CONFIG = 'config/'
DIR_INDEX = 'inverted_index/'
DIR_STATS = 'stats/'
FILE_EVENTS = DIR_CONFIG + 'events.log'
FILE_ERRORS = DIR_CONFIG + 'errors.log'
FILE_CONFIG = DIR_CONFIG + 'config.ini'
FILE_DOC = DIR_CONFIG + 'Readme'
FILE_BASELINKS = DIR_LINKS + '0'
FILE_INDEX = 'inverted_index.json'

# Lists used to clean up links and keywords:
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

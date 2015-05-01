#!/usr/bin/python3

"""Define required data for crawler."""

from socket import setdefaulttimeout

from datetime import timedelta

setdefaulttimeout(30)

# Strings for directories and files:
DIR_LINKS = 'links/'
DIR_CONFIG = 'config/'
DIR_DATA = 'data/'
DIR_OUTPUT = 'output/'
DIR_INDEX = DIR_DATA + 'inverted_index/'
FILE_NEWS = DIR_CONFIG + 'events.log'
FILE_STATS = DIR_DATA + 'stats_links.txt'
FILE_STATS2 = DIR_DATA + 'stats_stopwords.txt'
FILE_ERROR = DIR_CONFIG + 'errors.log'
FILE_CONFIG = DIR_CONFIG + 'config.ini'
FILE_DOC = DIR_CONFIG + 'Readme'
FILE_BASELINKS = DIR_LINKS + '0'
FILE_INDEX = DIR_DATA + 'inverted_index.json'

# Strings for ftp location
FTP_INDEX = '/www/data/inverted-index/'

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
CRAWL_DELAY = timedelta(days=2)  # The program don't crawl the website if it was crawled x ago
TIMEOUT = 30

# README :
README = """----- Documentation -----

In the first run, the crawler for swiftea ask what links start crawling.
So you can fill a fichier named '0' without extention with 10 links max,
or let program choose a list of links.

--- errors code: ---
	0 : end
	1 : event file not found in check_size
	2 : errors file not found in check_size
	3 :
	4 : fichier lecture introuvable dans get_url, stop
	5 : erreur compteur liens dans get_url, continue

	6 : erreur de connexion au site web (ConnectionError)
	7 : le site ne répond pas, continue
	8 : erreur inconue de connexion au site web, stop
	9 : pas d'indication d'encodage : encodage en utf-8, problèmes d'encodage possibles

	10 :  erreur de recupération des stopwords
	11 : erreur handle_entityref, continue

	12 : erreur de connexion à la base de données, ConnectionRefusedError, stop
	13 : erreur de connexion à la base de données, err.OperationalError, stop
	14 : erreur de connexion à la base de données (socket.timeout)
	15 : erreur inconu de connection à la base de données
	16 : erreur d'enregistrement dans la base : socket.timeout ou err.OperationalError
	17 : le documment n'a pas été supprimé
	18 : erreur de récupération de l'id0
	19 : aucune connexion avec la BDD

	20 : erreur de connexion au serveur ftp
	21 : erreur d'envoie de l'index inversé, continue
	22 : erreur de téléchargement de l'index inversé

	23 : Indexation trop longue

	24 : error robot.txt

	25 : error allowed

--- config file : ---
Le fichier config.txt doit être dans le dossier 'config', il est créé s'il n'existe pas.
Son contenu :
The file config.ini is in 'config' directory, it is create if doesn't exists.
It content is:
 - run = True or False
 - reading_file_number = number, program take links in this file
 - reading_line_number = number, the line in the file where program take links
 - writing_file_number = number, program save found links in this file
 - links_number = around the number

---fichier journal.log : ---
 - copie de ce qui s'affiche dans la console
 - auto-suppression quand il dépasse 500 Ko

---fichier erreur.log: ---
 - contient le rapport de chaque erreur recontrée
 - auto-suppression quand il dépasse 500 Ko

---fichier stats_links.txt et  stats_stopwords.txt: ---
 - contient les nombres de liens trouvé dans une page et le pourcentage de stopwords supprimés
 - lancer le fichier statistiques.py
 - ne pas supprimer

---fichier liens de base : ---
 - doit être dans le dossier 'liens'
"""

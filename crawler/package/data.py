#!/usr/bin/python3

"""Data for crawler."""

from datetime import timedelta

__author__ = "Seva Nathan"


# strings for directories and files :
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
FILE_CAN_SEND = DIR_DATA + 'can_send.json'

# strings for ftp location
FTP_INDEX = '/www/data/inverted-index/'

# lists for clean up links and keywords :
BAD_EXTENTIONS = ('.pdf', '.doc', '.xls', '.zip', '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico', '.svg', '.tiff', '.tif' '.raw', '.flv', '.mpeg', '.mpg', '.wma', '.mp4', '.mp3', '.fla', '.avi')
IMG_EXTENTIONS = ('.jpeg', '.jpg', '.png', '.gif', '.bmp', '.ico')
START_CHARS = ('«', '\'', '"', '(', ':', '/' , '[', '{', '-')
END_CHARS = ('.', ',', ';', '!', '?', '»', '\'', '"', ')', ':', '...', '/', ']', '}', '-')

# others informations :
USER_AGENT = 'Swiftea-Bot'
HEADERS = {"User-Agent": USER_AGENT}
MAX_SIZE = 500 # max size of a error and log file (FILE_ERROR and FILE_NEWS)
INDEXING_TIMEOUT = 120 # time in second for index a document
MAX_LINKS = 5000 # max links in a file
CRAWL_DELAY = timedelta(days=2) # the program don't crawl the website if it was crawled x ago
CRAWL_IMG_DELAY = timedelta(days=15)
TIMEOUT = 30

# README :
README = """----- Documentation -----

Le robot crawler pour Swfitea demande lors de la 1er exécution avec quels liens de départ démmarer le crawler.
On a donc le choix entre remplir un fichier '0' sans extention,
de liens de départ ou de laisser le programme récupérer une liste de liens de départ.
Si le dossier des liens est inexistant, le programme demanderra aussi
avec quelle liens de départ commencer.

---codes erreurs : ---
	0 : fin du programme
	1 : fichier journal introuvable dans check_size
	2 : fichier erreurs introuvable dans check_size
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

	25 : failed to update image

---fichier config.ini : ---
Le fichier config.txt doit être dans le dossier 'config', il est créé s'il n'existe pas.
Son contenu :
 - run = True ou False
 - reading_file_number = un nombre, le fichier où on prend les urls
 - reading_line_number = un nombre, le numéro du lien que l'on examine
 - writing_file_number = un nombre, le fichier où on enregistre les liens trouvés
 - links_number = un nombre, environ le nombre maximal de liens dans un fichier

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

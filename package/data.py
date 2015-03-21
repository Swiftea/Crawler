#!/usr/bin/python

"""data for crawler"""

__author__ = "Seva Nathan"

from socket import setdefaulttimeout # set the timeout

__author__ = "Seva Nathan"

setdefaulttimeout(30) # timeout is 30sec

# strings for direcories and files :
DIR_LINKS = 'liens/'
DIR_CONFIG = 'config/'
DIR_DATA = 'data/'
FILE_ARCHIVE_NEWS = DIR_DATA + 'archive_news.zip'
FILE_ARCHIVE_ERRORS = DIR_DATA + 'archive_errors.zip'
FILE_NEWS = DIR_CONFIG + 'journal.log'
FILE_STATS = DIR_DATA + 'stats_links.txt'
FILE_STATS2 = DIR_DATA + 'stats_stopwords.txt'
FILE_ERROR = DIR_CONFIG + 'erreur.log'
FILE_CONFIG = DIR_CONFIG + 'config.ini'
FILE_DOC = DIR_CONFIG + 'Readme'
FILE_BASELINKS = DIR_LINKS + '0'
FILE_INDEX = DIR_DATA + 'inverted_index.txt'
FILE_CAN_SEND = DIR_DATA + 'can_send.json'

# strings for ftp location
FTP_INDEX = '/www/data/inverted-index/inverted-index.txt'
FTP_CAN_SEND = '/www/data/can_send.json'

# lists for clean up links and keywords :
BAD_EXTENTIONS = ['.pdf', '.doc', '.xls', '.zip', '.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico', '.svg', '.tiff', '.tif' '.raw', '.flv', '.mpeg', '.mpg', '.wma', '.mp4', '.mp3', '.fla', '.avi']
START_CHARS = ['«', '\'', '"', '(', ':', '/' , '[', '{', '-']
END_CHARS = ['.', ',', ';', '!', '?', '»', '\'', '"', ')', ':', '...', '/', ']', '}', '-']

# others informations :
USER_AGENT = 'Swiftea-Bot'
MAX_SIZE = 500
TIMEOUT_INDEX = 120
HEADERS = {"User-Agent": USER_AGENT}
LINKS_NUMBER = 5000

# doc (read me):
DOC = """----- Documentation -----

Le robot crawler pour Swfitea demande lors de la 1er exécution avec quels
liens de départ démmarer le crawler. On a donc le choix entre remplir un
fichier '0' sans extention, de liens de départ ou de laisser le programme
récupérer une liste de liens de départ.
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

---fichier config.txt : ---
Le fichier config.txt doit être dans le dossier 'config',
il est créé s'il n'existe pas.
Son contenu : 
 - arrêt = 'continue' ou 'stop'
 - compteur fichier lecture = un nombre, le fichier où on prend les URLs
 - compteur liens = un nombre, le numéro du lien que l'on examine
 - compteur fichier écriture = un nombre, le fichier où on enregistre les liens trouvés
 - nombre de liens dans un fichier = un nombre, environ le nombre de liens dans un fichier
Exemple : "
arrêt : no
compteur fichier lecture : 0
compteur liens : 0
compteur fichier écriture : 1
nombre de liens dans un fichier : 500
"

---fichier journal.txt : ---
 - copie de ce qui s'affiche dans la console
 - auto-suppression quand il dépasse 500 Ko

---fichier erreur.txt: ---
 - contient le rapport de chaque erreur recontré
 - possibilité de le supprimé

---fichier stats.txt : ---
 - contient les nombres de liens trouvé dans une page
 - lancer le fichier statistiques pour avoir la moyenne et bientôt d'autre statistiques
 - ne pas supprimer

---fichier liens de base : ---
 - doit être dans le dossier 'liens'
"""

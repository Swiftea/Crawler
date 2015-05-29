#!/usr/bin/python3

from shutil import rmtree

from swiftea_bot.data import DIR_DATA, DIR_OUTPUT, DIR_LINKS, DIR_CONFIG

BASE_LINKS = """http://swiftea.alwaysdata.net/0
http://swiftea.alwaysdata.net/1
http://swiftea.alwaysdata.net/2
http://swiftea.alwaysdata.net/3
http://swiftea.alwaysdata.net/4
http://swiftea.alwaysdata.net/5
http://swiftea.alwaysdata.net/6
http://swiftea.alwaysdata.net/7
http://swiftea.alwaysdata.net/8
http://swiftea.alwaysdata.net/9
http://swiftea.alwaysdata.net/10
http://swiftea.alwaysdata.net/11
http://swiftea.alwaysdata.net/12
http://swiftea.alwaysdata.net/13
http://swiftea.alwaysdata.net/14
"""

URL = "http://aetfiws.alwaysdata.net"

SUGGESTIONS = ['http://suggestions.net/page1.html', 'http://suggestions.net/page2.html']

CODE1 = """<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="Description" content="Moteur de recherche">
        <title>Swiftea</title>
        <link rel="stylesheet" href="public/css/reset.css">
        <link rel="icon" href="public/favicon.ico" type="image/x-icon">
    </head>
    <body>
        <a href="demo">CSS Demo</a>
        <h1>Gros titre</h1>
        <h2>Moyen titre</h2>
        <h3>petit titre</h3>
        <p><strong>strong </strong><em>em</em></p>
        <a href="index">
            <img src="public/themes/default/img/logo.png" alt="Swiftea">
        </a>
        <a href="about/ninf.php" rel="noindex, nofollow">Why use Swiftea ?</a>
        <a href="about/ni.php" rel="noindex">Why use Swiftea ?</a>
        <a href="about/nf.php" rel="nofollow">Why use Swiftea ?</a>
        <img src="public/themes/default/img/github.png" alt="Github Swiftea">
        <img src="public/themes/default/img/twitter.png" alt="Twitter Swiftea">
    </body>
</html>
"""

CODE2 = """<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="content-language" content="en">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-16 LE" />
        <link rel="shortcut icon" href="public/favicon2.ico" type="image/x-icon">
    </head>
    <body>
    </body>
</html>
"""

CODE3 = """<!DOCTYPE html>
<html>
    <head>
        <meta name="language" content="fr">
    </head>
    <body>
    </body>
</html>
"""

INVERTED_INDEX = {'EN': {
'A': {'ab': {'above': {1: .3, 2: .1}, 'abort': {1: .3, 2: .1}}},
'W': {'wo': {'word': {1: .3, 30: .4}}}}, 'FR': {
'B': {'ba': {'bateau': {1: .5}}, 'bo': {'boule': {1: .25, 2: .8}}}}}

def reset():
    rmtree(DIR_DATA)
    rmtree(DIR_CONFIG)
    rmtree(DIR_OUTPUT)
    rmtree(DIR_LINKS)

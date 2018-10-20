#!/usr/bin/env python3

from shutil import rmtree
from os import remove

from swiftea_bot.data import DIR_DATA, BASE_LINKS


URL = "http://aetfiws.ovh"

SUGGESTIONS = ['http://suggestions.ovh/page1.html', 'http://suggestions.ovh/page2.html']

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
        <p>une <a href="demo">CSS Demo</a> ici!</p>
        <h1>Gros titre🤣 </h1>
        <h2>Moyen titre</h2>
        <h3>petit titre</h3>
        <p><strong>strong </strong><em>em</em></p>
        <a href="index">
            <img src="public/themes/default/img/logo.png" alt="Swiftea">
        </a>
        du texte au milieu
        <a href="about/ninf.php" rel="noindex, nofollow">Why use Swiftea ?1</a>
        <a href="about/ni.php" rel="noindex">Why use Swiftea ?2</a>
        <a href="about/nf.php" rel="nofollow">Why use Swiftea ?3</a>
        <img src="public/themes/default/img/github.png" alt="Github Swiftea">
        <img src="public/themes/default/img/twitter.png" alt="Twitter Swiftea">
        <p>&#0169;</p>
        <p>&gt;</p>
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
    try: rmtree(DIR_DATA)
    except FileNotFoundError: pass
    try: remove('test_RedirectOutput.ext')
    except FileNotFoundError: pass

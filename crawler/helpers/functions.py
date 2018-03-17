#!/usr/bin/python3

import sys
from urllib.parse import urlparse, urljoin

def clean_text(text):
    return text.strip() if (type(text) is str) else ''

def clean_url(url):
    url = url.strip()
    infos = urlparse(url)
    if infos.scheme in ['http', 'https']:
        url = infos.scheme + '://' + infos.netloc + infos.path
        if url[-1] == '/':
            url = url[:-1]
        if len(url) > 8 and len(url) <= 255:
            return url
        else:
            return None
    else:
        return None

def rebuild_url(url, origin):
    return urljoin(origin, url) # relative to absolute

def base_url(url):
    parsed_url = urlparse(url)
    base_url = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)

    return base_url

def close():
    sys.exit()

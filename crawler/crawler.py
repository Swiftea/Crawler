#!/usr/bin/python3

import logging
import requests
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from reppy.cache import RobotsCache

from parsers import *
from helpers.functions import base_url

class Crawler:
    def __init__(self, db_manager, config, url):
        self.db_manager = db_manager
        self.logger = logging.getLogger('crawler.Crawler')
        self.url = url
        self.config = config

    def crawl(self):
        response = self.query()

        if response is not None:
            url_type = self.characterize_url()
            self.logger.info('Type: %s', url_type)

            html = BeautifulSoup(response.text, 'lxml')

            parser_name = url_type.capitalize() + 'Parser'
            parser = globals()[parser_name](html, self.url)

            data = parser.get_data()

            if data is not None:
                return data
            else:
                self.logger.info('Miss infos to add data')
                return None
        else:
            return None

    def characterize_url(self):
        infos = urlparse(self.url)
        url_type = 'webpage'

        if '.wikipedia.org/wiki/' in self.url:
            if ':' not in infos.path:
                url_type = 'wikipedia'
        elif '.youtube.com/watch?v=' in self.url or '.youtube.com/channel/' in self.url:
            url_type = 'youtube'

        return url_type

    def query(self):
        try:
            robots = RobotsCache()
            rules = robots.fetch(base_url(self.url))

            if rules.allowed(self.url, self.config['default']['user_agent']):
                response = requests.get(self.url)
                if 'text/html' in response.headers['content-type']:
                    self.logger.info('Requests -> Get response')
                    return response
                else:
                    self.logger.info('Requests -> Unauthorized document type')
                    return None
            else:
                self.logger.info('Reppy -> Can\'t crawl (robots.txt)')
                return None
        except requests.exceptions.RequestException as error:
            self.logger.error(error)

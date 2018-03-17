#!/usr/bin/python3

import logging
import logging.config
import json
import socket
import atexit

from database.manager import DBManager
from urls_storage import URLSStorage
from crawler import Crawler
from initialize import Initialize

class Main:
    def __init__(self, urls):
        # Initialize folders and files
        Initialize(urls)

        # Logger
        logging.config.fileConfig('config/logging.ini')
        self.logger = logging.getLogger("crawler")

        # Import config
        with open('config/app.json', 'r') as f:
            self.config = json.load(f)

        # Timeout
        socket.setdefaulttimeout(self.config['request']['timeout'])

        self.logger.info('Crawler started')

        # Database
        self.db_manager = DBManager(self.config['database'])

        # Urls
        self.urls_storage = URLSStorage(self.config['crawl']['items_per_loop'])
        self.urls = self.urls_storage.get_urls()

    def launch(self):
        while True:
            urls = list()
            db_data = list()
            for url in self.urls:
                self.logger.info('Crawl %s', url)
                crawler = Crawler(self.db_manager, self.config, url)
                data = crawler.crawl()
                if data is not None:
                    urls.extend(data['urls'])
                    db_data.append(data)
                    self.logger.debug('Title: %s', data['data']['title'])

                self.logger.info('End crawl')

            # Send data to database
            self.db_manager.connect()
            for data in db_data:
                self.db_manager.insert(data)
            self.db_manager.close()

            # Urls
            self.urls = self.urls_storage.manage(urls)

    def stop(self):
        self.logger.info('Crawler stopped')

if __name__ == '__main__':
    urls = [
        'https://www.python.org',
        'https://fr.wikipedia.org/wiki/Python_(langage)',
        'https://pypi.python.org',
    ]

    main = Main(urls)
    atexit.register(main.stop)
    main.launch()
    main.stop()

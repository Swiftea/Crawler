#!/usr/bin/python3

import logging
import gzip
from os import remove
import json

class URLSStorage:
    def __init__(self, items_per_loop):
        self.logger = logging.getLogger('crawler.URLSStorage')
        self.items_per_loop = items_per_loop
        self.get_progress()

    def manage(self, urls):
        self.save_urls(urls, self.write_file)
        urls = self.get_urls()
        self.write_file += 1
        self.save_progress(self.read_file, self.write_file)
        return urls

    def get_urls(self):
        """Return the nb next urls from the file.
        Check for last line, remove file."""
        with gzip.open('data/urls/' + str(self.read_file) + '.gz', mode='rb') as f:
            content = f.read()

        content = content.decode(errors="replace")
        content = content.split('\n')
        urls = content[:self.items_per_loop]

        if urls == ['']:
            remove('data/urls/' + str(self.read_file) + '.gz')
            self.read_file += 1
            return self.get_urls()
        else:
            content = content[self.items_per_loop:]
            self.save_urls(content, self.read_file)
            return urls

    def save_urls(self, urls, write_file):
        """Save all urls in a new file.
        urls : list"""
        content = '\n'.join(urls)
        content = content.encode(errors="replace")
        with gzip.open('data/urls/' + str(write_file) + '.gz', mode='wb') as f:
            f.write(content)

    def get_progress(self):
        with open('save/urls.json', 'r') as f:
            save = json.load(f)
        self.read_file = save['read_file']
        self.write_file = save['write_file']

    def save_progress(self, read_file, write_file):
        save = dict()
        save['read_file'] = read_file
        save['write_file'] = write_file
        with open('save/urls.json', 'w') as f:
            json.dump(save, f)

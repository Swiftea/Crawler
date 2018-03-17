#!/usr/bin/python3

import os

from urls_storage import URLSStorage

class Initialize:
    def __init__(self, urls):
        self.directories = ['logs', 'save', 'data', 'data/urls']
        self.urls = urls
        self.start()

    def start(self):
        self.check_dirs()
        self.check_save_urls()
        self.check_urls()

    def check_dirs(self):
        for path in self.directories:
            if not os.path.isdir(path):
                os.mkdir(path)

    def check_save_urls(self):
        if not os.path.exists('save/urls.json'):
            URLSStorage.save_progress(self, 0, 0)

    def check_urls(self):
        if not os.path.exists('data/urls/0.gz'):
            URLSStorage.save_urls(self, self.urls, 0)

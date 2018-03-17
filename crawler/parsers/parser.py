#!/usr/bin/python3

from helpers.functions import clean_text, rebuild_url, clean_url

class Parser:
    def __init__(self, html, url):
        self.html = html
        self.url = url
        self.data = dict()

    def language(self):
        language = self.html.find('html')
        if language and language.has_attr('lang'):
            return clean_text(language['lang'])
        else:
            return ''

    def links(self):
        urls = []
        for link in self.html.find_all('a'):
            url = rebuild_url(link.get('href'), self.url)
            url = clean_url(url)
            if url is not None:
                if url not in urls:
                    urls.append(url)
        return urls

    def get_data(self):
        self.data['data'] = dict()
        self.data['data']['url'] = self.url
        self.data['data']['language'] = self.language()
        self.data['urls'] = self.links()
        self.get_other_data()

        if None in self.data['data'].values():
            return None
        else:
            return self.data

#!/usr/bin/python3

from parsers.parser import Parser
from helpers.functions import clean_text

class WebpageParser(Parser):
    def __init__(self, html, url):
        Parser.__init__(self, html, url)
        self.html = html
        self.url = url

    def title(self):
        title = self.html.title
        return clean_text(title.text) if title else None

    def description(self):
        meta = self.html.find(attrs={'name':'description'})

        if meta:
            return clean_text(meta['content'])
        else:
            h1 = self.html.find('h1')
            if h1:
                return clean_text(h1.text)
            else:
                return ''

    def get_other_data(self):
        self.data['type'] = 'webpage'
        self.data['data']['title'] = self.title()
        self.data['data']['description'] = self.description()

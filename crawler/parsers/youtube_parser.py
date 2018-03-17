#!/usr/bin/python3

from parsers.parser import Parser
from helpers.functions import clean_text

class YoutubeParser(Parser):
    def __init__(self, html, url):
        Parser.__init__(self, html, url)
        self.html = html
        self.url = url


    def title(self):
        title = self.html.title
        return clean_text(title.text.split('- YouTube')[0]) if title else None

    def code(self):
        code = self.url[32:]
        return code

    def get_other_data(self):
        self.data['type'] = 'youtube'
        self.data['data']['title'] = self.title()
        self.data['data']['code'] = self.code()

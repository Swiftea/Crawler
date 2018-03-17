#!/usr/bin/python3

import textwrap

from parsers.parser import Parser
from helpers.functions import clean_text

class WikipediaParser(Parser):
    def __init__(self, html, url):
        Parser.__init__(self, html, url)
        self.html = html
        self.url = url

    def title(self):
        title = self.html.title
        return clean_text(title.text.split('—')[0]) if title else None

    def summary(self, words):
        summary = self.html.find('div', id='mw-content-text').find('p', recursive=False)
        if summary:
            summary = textwrap.shorten(summary.text, width=words, placeholder="...")
            return clean_text(summary)
        else:
            return None

    def get_other_data(self):
        self.data['type'] = 'wikipedia'
        self.data['data']['title'] = self.title()
        self.data['data']['summary'] = self.summary(200)

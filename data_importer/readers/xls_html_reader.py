#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


class XLSHTMLReader(object):
    def __init__(self, instance):
        self.instance = instance

    def read(self):
        html = open(u'{}'.format(self.instance.source), 'rb')
        beautiful_soup = BeautifulSoup(html, 'html.parser')
        main_table = beautiful_soup.find(self.instance.table_selector)
        for tr in main_table.find_all('tr'):
            values = [self.clean_td(td.string) for td in tr.find_all('td')]
            if values:
                yield values

    @classmethod
    def clean_td(cls, string):
        return string.replace('\n', '')

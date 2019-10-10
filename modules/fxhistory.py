from __future__ import absolute_import
from __future__ import print_function

import os
import json
import datetime

from modules.parser import Parser
from modules.crawler import Crawler

parser = Parser()
crawler = Crawler()

class FxHistory:
    def __init__(self):
        self.history = {}
        self.load()

        crawler.get(file='.tmp.csv')
        self.history.update(parser.get(file='.tmp.csv'))
        os.remove('.tmp.csv')

        self.dump()

    def load(self):
        files = os.listdir('data/')
        for file in files:
            with open('data/' + file, 'r') as file:
                self.history.update(json.load(file))

    def dump(self):
        years = list(set([key[:key.find('/')] for key in self.history.keys()]))
        for year in years:
            data = {}
            for date in self.history.keys():
                if date[:date.find('/')] == year:
                    data[date] = self.history[date]
            with open('data/' + year + '.json', 'w') as file:
                json.dump(data, file)

    def list(self):
        pass
        
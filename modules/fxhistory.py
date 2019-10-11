from __future__ import absolute_import
from __future__ import print_function

import os
import json
import datetime

from datetime import timedelta

from modules.parser import Parser
from modules.crawler import Crawler

parser = Parser()
crawler = Crawler()

__url__ = 'http://www.taifex.com.tw/data_gov/taifex_open_data.asp?data_name=DailyForeignExchangeRates'

class FxHistory:
    def __init__(self):
        self.history = {}
        self.load()
        self.update(input=__url__)

    def update(self, **kwargs):
        if 'http' in kwargs['input']:
            crawler.get(url=kwargs['input'], file='.tmp.csv')
            self.history.update(parser.get(file='.tmp.csv'))
            os.remove('.tmp.csv')
        else:
            self.history.update(parser.get(file=kwargs['input']))
        self.dump()

    def load(self):
        files = sorted(os.listdir('data/'))
        for file in files:
            with open('data/' + file, 'r') as file:
                self.history.update(json.load(file))

    def dump(self):
        years = list(set([key[:4] for key in self.history.keys()]))
        for year in years:
            data = {}
            for date in self.history.keys():
                if date[:4] == year:
                    data[date] = self.history[date]
            with open('data/' + year + '.json', 'w') as file:
                json.dump(data, file)

    def list(self, **kwargs):
        ret = {}
        dates = self.history.keys()
        for index in range(0, (kwargs['end'] - kwargs['start']).days):
            date = kwargs['start'] + timedelta(index)
            date = date.strftime('%Y%m%d')
            if date in dates:
                ret[date] = {}
                for currency in kwargs['currency']:
                    try:
                        ret[date][currency] = self.history[date][currency]
                    except:
                        ret[date][currency] = '-'
        return ret
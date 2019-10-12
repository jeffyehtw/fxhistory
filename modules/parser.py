from __future__ import absolute_import
from __future__ import print_function

import os
import csv
import json
import datetime

from modules.define import Define

define = Define()

class Parser:
    def __init__(self):
        self.headers = [
            'date', 'USD/TWD', 'CYN/TWD', 'EUR/USD', 'USD/JPY', 'GBP/USD',
            'AUD/USD','USD/HKD', 'USD/CYN', 'USD/ZAR', 'NZD/USD'
        ]

    def format(self, **kwargs):
        with open(kwargs['file'], 'r', encoding='big5') as file:
            lines = file.readlines()

        for key in define.mapping.keys():
            lines[0] = lines[0].replace(define.mapping[key], key)

        lines = [line.replace('／', '/') for line in lines]
        lines[0] = lines[0].replace('日期', 'date')

        if ','.join(self.headers) != lines[0][:-1]:
            print('[ERROR] Invalid data')
            exit()

        with open(kwargs['file'], 'w', encoding='utf-8') as file:
            file.writelines(lines)

    def get(self, **kwargs):
        self.format(file=kwargs['file'])

        raw_data = {}
        with open(kwargs['file'], 'r') as file:
            rows = csv.reader(file)
            next(rows)
            raw_data = {row[0]: dict(zip(self.headers[1:], row[1:])) for row in rows}

        # remove duplicated CYN
        for date in raw_data.keys():
            raw_data[date].pop('CYN/TWD')

        dates = list(raw_data.keys())
        for date in dates:
            new_date = datetime.datetime.strptime(date, '%Y/%m/%d')
            new_date = new_date.strftime('%Y%m%d')
            raw_data[new_date] = raw_data.pop(date)

        data = {}
        for date in raw_data.keys():
            data[date] = {}
            data[date]['USD'] = '1'
            for key in raw_data[date].keys():
                currency = key.split('/')
                try:
                    rate = float(raw_data[date][key])
                    if currency[0] == 'USD':
                        data[date][currency[1]] = str(rate)
                    else:
                        data[date][currency[0]] = str(1 / rate)
                except:
                    continue
        return data
from __future__ import absolute_import
from __future__ import print_function

import os
import csv
import json

class Parser:
    def __init__(self):
        self.headers = [
            'date', 'USD/TWD', 'CYN/TWD', 'EUR/USD', 'USD/JPY', 'GBP/USD',
            'AUD/USD','USD/HKD', 'USD/CYN', 'USD/ZAR', 'NZD/USD'
        ]
        self.currency = {
            'USD': '美元',
            'CYN': '人民幣',
            'EUR': '歐元',
            'JPY': '日幣',
            'GBP': '英鎊',
            'AUD': '澳幣',
            'HKD': '港幣',
            'ZAR': '南非幣',
            'NZD': '紐幣',
            'TWD': '新台幣',
        }
    
    def format(self, **kwargs):
        with open(kwargs['file'], 'r', encoding='big5') as file:
            lines = file.readlines()

        for key in self.currency.keys():
            lines[0] = lines[0].replace(self.currency[key], key)

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
            for currency in raw_data[date].keys():
                raw_data[date][currency] = float(raw_data[date][currency])

        data = {}
        for date in raw_data.keys():
            data[date] = {}
            for key in raw_data[date].keys():
                currency = key.split('/')
                if currency[0] == 'USD':
                    data[date][currency[1]] = raw_data[date][key]
                else:
                    data[date][currency[0]] = 1 / raw_data[date][key]

        return data

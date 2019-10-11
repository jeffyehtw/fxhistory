from __future__ import absolute_import
from __future__ import print_function

class Strings:
    def __init__(self):
        self.date_help = '20190101'
        self.command_help = 'choices: {command}'
        self.currency_help = 'choices: {currency}'

class Define:
    def __init__(self):
        self.strings = Strings()
        self.currency = [
            'CYN', 'EUR', 'JPY', 'GBP', 'AUD',
            'HKD', 'ZAR', 'NZD', 'TWD'
        ]
        self.mapping = {
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
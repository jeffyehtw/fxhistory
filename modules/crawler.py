from __future__ import absolute_import
from __future__ import print_function

import os
import requests

__url__ = 'http://www.taifex.com.tw/data_gov/taifex_open_data.asp?data_name=DailyForeignExchangeRates'

class Crawler:
    def __init__(self):
        pass

    def get(self, **kwargs):
        with open(kwargs['file'], 'wb') as file:
            response = requests.get(__url__)
            file.write(response.content)
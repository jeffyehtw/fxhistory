from __future__ import absolute_import
from __future__ import print_function

import os
import requests

class Crawler:
    def __init__(self):
        pass

    def get(self, **kwargs):
        with open(kwargs['file'], 'wb') as file:
            response = requests.get(kwargs['url'])
            file.write(response.content)
from __future__ import absolute_import
from __future__ import print_function

import numpy

def isfloat(s):
    try:
        float(s)
        return True
    except:
        return False

class Statistics:
    def __init__(self):
        pass

    def calculate(self, **kwargs):
        ret = {}
        for currency in kwargs['currency']:
            dates = list(kwargs['data'].keys())
            data = [float(kwargs['data'][date][currency]) for date in dates if isfloat(kwargs['data'][date][currency])]
            ret[currency] = {
                'min': str(numpy.min(data)) if len(data) > 0 else '-',
                'max': str(numpy.max(data)) if len(data) > 0 else '-',
                'mean': str(numpy.mean(data)) if len(data) > 0 else '-'
            }

        return ret



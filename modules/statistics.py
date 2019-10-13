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

    def kd(self, **kwargs):
        N = 9
        A = 1 / 3
        high = [0] * (N - 1)
        low = [0] * (N - 1)
        rsv = [0] * (N - 1)
        k = [0] * (N - 2) + [50]
        d = [0] * (N - 2) + [50]

        for i in range(N - 1, len(kwargs['data'])):
            array = kwargs['data'][max(0, i - N + 1):i + 1]
            low.append(numpy.min(array))
            high.append(numpy.max(array))

        for i in range(N - 1, len(kwargs['data'])):
            rsv.append((kwargs['data'][i] - low[i]) / (high[i] - low[i]) * 100)
            k.append(A * rsv[i] + (1 - A) * k[i - 1])
            d.append(A * k[i] + (1 - A) * d[i - 1])

        return {
            'k': k,
            'd': d
        }



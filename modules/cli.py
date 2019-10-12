from __future__ import absolute_import
from __future__ import print_function

import sys
import numpy
import argparse
import datetime

from datetime import timedelta
from tabulate import tabulate
from matplotlib import pyplot

from modules.define import Define
from modules.fxhistory import FxHistory
from modules.statistics import Statistics

# constant
__version__ = '1.1'
__description__ = 'A command line tool for foreign exchange'
__epilog__ = 'Report bugs to <yehcj.tw@gmail.com>'

define = Define()
fxhistory = FxHistory()
statistics = Statistics()

class Cli:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description=__description__,
            epilog=__epilog__
        )
        parser.add_argument('command', help=define.strings.command_help.format(
            command='list,state'
        ))
        parser.add_argument(
            '-v', '-V', '--version',
            action='version',
            help='show version of program',
            version='v{}'.format(__version__)
        )
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecongnized command')
            parser.print_help()
            exit()

        getattr(self, args.command)()

    def update(self):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument(
            'input',
            help=''
        )
        args = parser.parse_args(sys.argv[2:])
        fxhistory.update(input=args.input)

    def state(self):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument(
            '-d', '--date',
            nargs='+',
            default=[
                (datetime.datetime.now() - timedelta(30)).strftime('%Y%m%d'),
                datetime.datetime.now().strftime('%Y%m%d'),
            ],
            help=define.strings.date_help
        )
        parser.add_argument(
            '-c', '--currency',
            nargs='+',
            default=define.currency,
            help=define.strings.currency_help.format(
                currency=', '.join(define.currency)
            )
        )

        args = parser.parse_args(sys.argv[2:])
        args.date[0] = datetime.datetime.strptime(args.date[0], '%Y%m%d')
        args.date[1] = datetime.datetime.strptime(args.date[1], '%Y%m%d')

        data = fxhistory.list(
            start=args.date[0],
            end=args.date[1],
            currency=args.currency
        )
        stat = statistics.calculate(
            data=data,
            currency=args.currency
        )

        table = []
        headers = ['currency'] + list(stat[list(stat)[0]].keys())
        for currency in stat.keys():
            table.append([currency] + [stat[currency][x] for x in headers[1:]])
        print(tabulate(table, headers=headers, tablefmt='github'))

    def list(self):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument(
            '-d', '--date',
            nargs='+',
            default=[
                (datetime.datetime.now() - timedelta(30)).strftime('%Y%m%d'),
                datetime.datetime.now().strftime('%Y%m%d'),
            ],
            help=define.strings.date_help
        )
        parser.add_argument(
            '-c', '--currency',
            nargs='+',
            default=define.currency,
            choices=define.currency,
            metavar='CURRENCY',
            help=define.strings.currency_help.format(
                currency=', '.join(define.currency)
            )
        )
        parser.add_argument(
            '-b', '--base',
            default='TWD',
            choices=define.currency,
            help='base'
        )

        args = parser.parse_args(sys.argv[2:])
        try:
            args.date[0] = datetime.datetime.strptime(args.date[0], '%Y%m%d')
            args.date[1] = datetime.datetime.strptime(args.date[1], '%Y%m%d')
        except:
            parser.print_help()
            exit()

        if args.date[0] > args.date[1]:
            parser.print_help()
            exit()

        data = fxhistory.list(
            start=args.date[0],
            end=args.date[1],
            currency=args.currency,
            base=args.base
        )

        table = []
        headers = ['date'] + args.currency
        for date in data.keys():
            table.append([date] + [data[date][x] for x in args.currency])
        print(tabulate(table, headers=headers, tablefmt='github'))

    def plot(self):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument(
            '-d', '--date',
            nargs='+',
            default=[
                (datetime.datetime.now() - timedelta(30)).strftime('%Y%m%d'),
                datetime.datetime.now().strftime('%Y%m%d'),
            ],
            help=define.strings.date_help
        )
        parser.add_argument(
            '-c', '--currency',
            nargs='+',
            default=define.currency,
            choices=define.currency,
            metavar='CURRENCY',
            help=define.strings.currency_help.format(
                currency=', '.join(define.currency)
            )
        )
        parser.add_argument(
            '-f', '--file',
            help='file'
        )
        parser.add_argument(
            '-t', '--type',
            choices=['trend', 'cdf'],
            default='line',
            help='type'
        )
        parser.add_argument(
            '-b', '--base',
            choices=define.currency,
            default='TWD',
            help='base'
        )

        args = parser.parse_args(sys.argv[2:])
        try:
            args.date[0] = datetime.datetime.strptime(args.date[0], '%Y%m%d')
            args.date[1] = datetime.datetime.strptime(args.date[1], '%Y%m%d')
        except:
            parser.print_help()
            exit()

        if args.date[0] > args.date[1]:
            parser.print_help()
            exit()

        data = fxhistory.list(
            start=args.date[0],
            end=args.date[1],
            currency=args.currency,
            base=args.base
        )

        if args.type == 'trend':
            for currency in args.currency:
                x = []
                y = []
                for date in data.keys():
                    try:
                        x.append(datetime.datetime.strptime(date, '%Y%m%d'))
                        y.append(float(data[date][currency]))
                    except:
                        pass

                pyplot.plot_date(x, y, 'o-')
                pyplot.gcf().autofmt_xdate()
                pyplot.title(currency + '/' + args.base)

                if args.file == None:
                    pyplot.show()
                else:
                    pyplot.savefig(args.file, dpi=300)

        elif args.type == 'cdf':
            for currency in args.currency:
                x = [float(data[date][currency]) for date in data.keys()]
                x = [numpy.percentile(x, index) for index in range(0, 100)]
                pyplot.plot(x, range(0, 100))
                pyplot.title(currency + '/' + args.base)

                if args.file == None:
                    pyplot.show()
                else:
                    pyplot.savefig(args.file, dpi=300)
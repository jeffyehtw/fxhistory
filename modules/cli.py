from __future__ import absolute_import
from __future__ import print_function

import sys
import argparse

from modules.fxhistory import FxHistory

# constant
__version__ = '1.0'
__description__ = 'A command line tool for foreign exchange'
__epilog__ = 'Report bugs to <yehcj.tw@gmail.com>'

class Cli:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description=__description__,
            epilog=__epilog__
        )

        parser.add_argument('command', help='list')

        parser.add_argument(
            '-v', '-V', '--version',
            action='version',
            help='show version of program',
            version='v{}'.format(__version__)
        )

        args = parser.parse_args(sys.argv[1:])

        if not hasattr(FxHistory(), args.command):
            print('Unrecongnized command')
            parser.print_help()
            exit()

        getattr(FxHistory(), args.command)()
 
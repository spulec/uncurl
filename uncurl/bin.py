from __future__ import print_function

import sys

from .api import parse


def main():
    result = parse(sys.argv[1])
    print(result)

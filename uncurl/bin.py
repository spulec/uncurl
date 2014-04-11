from __future__ import print_function

import sys

from .api import parse


def main():
    if sys.stdin.isatty():
        result = parse(sys.argv[1])
    else:
        result = parse(sys.stdin.read())
    print(result)

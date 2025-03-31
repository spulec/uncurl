# -*- coding: utf-8 -*-
import sys

try:
    from pyperclip import paste as clip_paste
except ImportError:

    def clip_paste():
        return list()


from .api import parse


def main():
    if sys.stdin.isatty():
        if len(sys.argv) > 1:
            # If an argument is passed
            result = parse(sys.argv[1:])
        else:
            # Otherwise pull from clipboard
            result = parse(clip_paste())
    else:
        result = parse(sys.stdin.read())
    print("\n" + result)


if __name__ == "__main__":
    main()

"""
Uncurl-X is a library that allows you to convert curl requests into python code that uses [httpx](https://www.python-httpx.org/). Since the Chrome network inspector has a nifty "Copy as cURL", this tool is useful for recreating browser requests in python.

When you don't pass any arguments to `uncurlx`, it will use whatever is in your clipboard as the curl command.

This is a fork of `uncurl` by `spulec` which converts from curl to `requests`.

"""

from .api import parse, parse_context

__version__ = "0.0.1"
__all__ = [parse, parse_context]

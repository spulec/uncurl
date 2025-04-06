# Uncurl-X - Converting curl requests to python httpx requests

![PyPI - Status](https://img.shields.io/pypi/status/uncurlx?style=flat-square&label=PyPI&)
![Python test Status](https://img.shields.io/github/actions/workflow/status/whichoneiwonder/uncurl-x/python-test.yml?label=Tests&style=flat-square)
![Dependencies Status](https://img.shields.io/github/actions/workflow/status/whichoneiwonder/uncurl-x/dependency-check.yml?label=deps-check&style=flat-square)
<!-- ![GitHub branch status](https://img.shields.io/github/checks-status/whichoneiwonder/uncurl-x/master?style=flat-square) -->
![GitHub License](https://img.shields.io/github/license/whichoneiwonder/uncurl-x?style=flat-square)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/whichoneiwonder/uncurl-x?style=flat-square)
![Format Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fastral-sh%2Fruff%2Fmain%2Fassets%2Fbadge%2Fv2.json&style=flat-square)


<!-- [![Build Status](https://travis-ci.org/spulec/uncurl.png?branch=master)](https://travis-ci.org/spulec/uncurl) -->

# In a nutshell

Uncurl-X is a library that allows you to convert curl requests into python code that uses [httpx](https://www.python-httpx.org/). Since the Chrome network inspector has a nifty "Copy as cURL", this tool is useful for recreating browser requests in python.

When you don't pass any arguments to `uncurlx`, it will use whatever is in your clipboard as the curl command.

This is a fork of [`uncurl`](https://github.com/spulec/uncurl) by `spulec` which converts from `curl` to `requests`.

## Example

```bash
$ uncurl "curl 'https://pypi.python.org/pypi/uncurlx' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Cache-Control: max-age=0' -H 'Cookie: foo=bar;' -H 'Connection: keep-alive' --compressed"
httpx.get("https://pypi.python.org/pypi/uncurlx", headers={
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
}, cookies={
    "foo": "bar",
})
```

The underlying API:

```python
import uncurlx

print(uncurlx.parse("curl 'https://pypi.python.org/pypi/uncurlx' -H 'Accept-Encoding: gzip,deflate,sdch'"))
```

prints the string

```bash
'requests.get("https://pypi.python.org/pypi/uncurlx", headers={
    "Accept-Encoding": "gzip,deflate,sdch",
})'
```

You can also retrieve the components as python objects:

```python
>>> import uncurlx
>>> context = uncurl.parse_context("curl 'https://pypi.python.org/pypi/uncurlx' -H 'Accept-Encoding: gzip,deflate,sdch'")
>>> context.url
https://pypi.python.org/pypi/uncurlx
>>> context.headers
OrderedDict([('Accept-Encoding', 'gzip,deflate,sdch')])
```
On Mac OS, you can also pipe input to uncurlx:

```bash
pbpaste | uncurlx
```

## Install

```console
$ pip install uncurlx
```

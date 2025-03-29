from unittest.mock import patch
import six
from uncurlx.__main__ import main

print_module = "__builtin__.print" if six.PY2 else "uncurlx.bin.print"


@patch("uncurl.bin.sys")
@patch(print_module)
def test_main(printer, fake_sys):
    fake_sys.argv = [
        "uncurlx",
        "curl 'https://pypi.python.org/pypi/uncurlx' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Accept-Language: en-US,en;q=0.8'",
    ]
    main()

    printer.assert_called_once_with(
        """
httpx.get("https://pypi.python.org/pypi/uncurlx",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "en-US,en;q=0.8"
    },
    cookies={},
    auth=(),
)"""
    )

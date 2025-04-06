import shlex
from unittest import TestCase
from unittest.mock import patch

from uncurlx.__main__ import main

print_module = "uncurlx.__main__.print"
sys_module = "uncurlx.__main__.sys"


class TestUncurlxMain(TestCase):
    @patch(sys_module)
    @patch(print_module)
    def test_main_method(self, printer, fake_sys):
        fake_sys.argv = [
            "uncurlx",
            *shlex.split(
                "curl 'https://pypi.python.org/pypi/uncurlx' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Accept-Language: en-US,en;q=0.8'"
            ),
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
    proxy={},
)"""
        )

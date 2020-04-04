from mock import patch
import six
from uncurl.bin import main

print_module = "__builtin__.print" if six.PY2 else "uncurl.bin.print"


@patch("uncurl.bin.sys")
@patch(print_module)
def test_main(printer, fake_sys):
    fake_sys.argv = ['uncurl', "curl 'https://pypi.python.org/pypi/uncurl' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Accept-Language: en-US,en;q=0.8'"]
    main()

    printer.assert_called_once_with(
        """
requests.get("https://pypi.python.org/pypi/uncurl",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "en-US,en;q=0.8"
    },
    cookies={},
)""")

from mock import patch

from uncurl.bin import main


@patch("uncurl.bin.sys")
@patch("__builtin__.print")
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

import sure

import uncurl


def test_basic_get():
    uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl'").should.equal(
        """requests.get("https://pypi.python.org/pypi/uncurl",
    headers={},
    cookies={},
)"""
    )


def test_basic_headers():
    uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Accept-Language: en-US,en;q=0.8'").should.equal(
        """requests.get("https://pypi.python.org/pypi/uncurl",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "en-US,en;q=0.8",
    },
    cookies={},
)"""
    )


def test_cookies():
    uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'").should.equal(
        """requests.get("https://pypi.python.org/pypi/uncurl",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
    },
    cookies={
        "baz": "baz2",
        "foo": "bar",
    },
)"""
    )


def test_cookies_lowercase():
    uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'cookie: foo=bar; baz=baz2'").should.equal(
        """requests.get("https://pypi.python.org/pypi/uncurl",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
    },
    cookies={
        "baz": "baz2",
        "foo": "bar",
    },
)"""
    )


def test_post():
    uncurl.parse("""curl 'https://pypi.python.org/pypi/uncurl' --data '[{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"},"now":1396219192277,"ab":{"welcome_email":{"v":"2","g":2}}}]' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'""").should.equal(
        """requests.post("https://pypi.python.org/pypi/uncurl",
    data='[{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"},"now":1396219192277,"ab":{"welcome_email":{"v":"2","g":2}}}]',
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
    },
    cookies={
        "baz": "baz2",
        "foo": "bar",
    },
)"""
    )


def test_post_with_dict_data():
    uncurl.parse("""curl 'https://pypi.python.org/pypi/uncurl' --data '{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"}}' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'""").should.equal(
        """requests.post("https://pypi.python.org/pypi/uncurl",
    data={
        "evt": "newsletter.show",
        "properties": {
            "newsletter_type": "userprofile",
        },
    },
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
    },
    cookies={
        "baz": "baz2",
        "foo": "bar",
    },
)"""
    )


def test_post_with_string_data():
    uncurl.parse("""curl 'https://pypi.python.org/pypi/uncurl' --data 'this is just some data'""").should.equal(
        """requests.post("https://pypi.python.org/pypi/uncurl",
    data='this is just some data',
    headers={},
    cookies={},
)"""
    )

def test_parse_curl_with_binary_data():
    uncurl.parse("""curl 'https://pypi.python.org/pypi/uncurl' --data-binary 'this is just some data'""").should.equal(
        """requests.post("https://pypi.python.org/pypi/uncurl",
    data='this is just some data',
    headers={},
    cookies={},
)"""
    )

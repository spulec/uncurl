import unittest  # noqa # Hey! Do not delete this import for the tests to pass

import uncurlx


OLD_ENDPOINT = "https://pypi.python.org/pypi/uncurlx"
ENDPOINT = "https://httpbin.org/anything"


class TestUncurlx(unittest.TestCase):
    def test_basic_get(self):
        output = uncurlx.parse(f"curl '{ENDPOINT}'")
        expected = (
            """httpx.get("{}",""".format(ENDPOINT)
            + """
    headers={},
    cookies={},
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_colon_header(self):
        output = uncurlx.parse(f"curl '{ENDPOINT}' -H 'authority:mobile.twitter.com'")
        expected = (
            """httpx.get("{}",""".format(ENDPOINT)
            + """
    headers={
        "authority": "mobile.twitter.com"
    },
    cookies={},
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_basic_headers(self):
        output = uncurlx.parse(
            f"curl '{ENDPOINT}' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Accept-Language: en-US,en;q=0.8'"
        )
        expected = (
            """httpx.get("{}",""".format(ENDPOINT)
            + """
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "en-US,en;q=0.8"
    },
    cookies={},
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_cookies(self):
        output = uncurlx.parse(
            f"curl '{ENDPOINT}' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'"
        )
        expected = (
            """httpx.get("{}",""".format(ENDPOINT)
            + """
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
    },
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_cookies_lowercase(self):
        output = uncurlx.parse(
            f"curl '{ENDPOINT}' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'cookie: foo=bar; baz=baz2'"
        )
        expected = (
            """httpx.get("{}",""".format(ENDPOINT)
            + """
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
    },
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_cookies_dollar_sign(self):
        output = uncurlx.parse(
            f"curl '{ENDPOINT}' -H 'Accept-Encoding: gzip,deflate,sdch' -H $'Cookie: somereallyreallylongcookie=true'"
        )
        expected = (
            """httpx.get("{}",""".format(ENDPOINT)
            + """
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "somereallyreallylongcookie": "true"
    },
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_post(self):
        output = uncurlx.parse(
            f"""curl '{ENDPOINT}'"""
            """ --data '[{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"},"now":1396219192277,"ab":{"welcome_email":{"v":"2","g":2}}}]' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'"""
        )
        expected = (
            """httpx.post("{}",""".format(ENDPOINT)
            + """
    data='[{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"},"now":1396219192277,"ab":{"welcome_email":{"v":"2","g":2}}}]',
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
        "Content-Type": "application/x-www-form-urlencoded"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
    },
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_post_with_dict_data(self):
        output = uncurlx.parse(
            f"""curl '{ENDPOINT}'"""
            """ --data '{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"}}' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'"""
        )
        expected = (
            """httpx.post("{}",""".format(ENDPOINT)
            + """
    data='{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"}}',
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
        "Content-Type": "application/x-www-form-urlencoded"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
    },
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_post_with_string_data(self):
        output = uncurlx.parse(
            f"""curl '{ENDPOINT}' """
            """--data 'this is just some data'"""
        )
        expected = (
            """httpx.post("{}",""".format(ENDPOINT)
            + """
    data='this is just some data',
    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    },
    cookies={},
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_parse_curl_with_binary_data(self):
        output = uncurlx.parse(
            f"""curl '{ENDPOINT}'"""
            """ --data-binary 'this is just some data'"""
        )
        expected = (
            """httpx.post("{}",""".format(ENDPOINT)
            + """
    data='this is just some data',
    headers={},
    cookies={},
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_parse_curl_with_raw_data(self):
        output = uncurlx.parse(
            f"""curl '{ENDPOINT}'"""
            """ --data-raw 'this is just some data'"""
        )
        expected = (
            """httpx.post("{}",""".format(ENDPOINT)
            + """
    data='this is just some data',
    headers={},
    cookies={},
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_parse_curl_with_another_binary_data(self):
        output = uncurlx.parse(
            r"""curl -H 'PID: 20000079' -H 'MT: 4' -H 'DivideVersion: 1.0' -H 'SupPhone: Redmi Note 3' -H 'SupFirm: 5.0.2' -H 'IMEI: wx_app' -H 'IMSI: wx_app' -H 'SessionId: ' -H 'CUID: wx_app' -H 'ProtocolVersion: 1.0' -H 'Sign: 7876480679c3cfe9ec0f82da290f0e0e' -H 'Accept: /' -H 'BodyEncryptType: 0' -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36 hap/1.0/oppo com.nearme.instant.platform/2.1.0beta1 com.felink.quickapp.reader/1.0.3 ({"packageName":"com.oppo.market","type":"other","extra":{}})' -H 'Content-Type: text/plain; charset=utf-8' -H 'Host: pandahomeios.ifjing.com' --data-binary '{"CateID":"508","PageIndex":1,"PageSize":30}' --compressed"""
            f""" '{ENDPOINT}/action.ashx/otheraction/9028'"""
        )
        expected = (
            f"""httpx.post("{ENDPOINT}/action.ashx/otheraction/9028","""
            r"""
    data='{"CateID":"508","PageIndex":1,"PageSize":30}',
    headers={
        "Accept": "/",
        "BodyEncryptType": "0",
        "CUID": "wx_app",
        "Content-Type": "text/plain; charset=utf-8",
        "DivideVersion": "1.0",
        "Host": "pandahomeios.ifjing.com",
        "IMEI": "wx_app",
        "IMSI": "wx_app",
        "MT": "4",
        "PID": "20000079",
        "ProtocolVersion": "1.0",
        "SessionId": "",
        "Sign": "7876480679c3cfe9ec0f82da290f0e0e",
        "SupFirm": "5.0.2",
        "SupPhone": "Redmi Note 3",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36 hap/1.0/oppo com.nearme.instant.platform/2.1.0beta1 com.felink.quickapp.reader/1.0.3 ({\"packageName\":\"com.oppo.market\",\"type\":\"other\",\"extra\":{}})"
    },
    cookies={},
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_parse_curl_with_insecure_flag(self):
        output = uncurlx.parse(f"""curl '{ENDPOINT}' --insecure""")
        expected = (
            """httpx.get("{}",""".format(ENDPOINT)
            + """
    headers={},
    cookies={},
    auth=(),
    proxy={},
    verify=False
)"""
        )
        self.assertEqual(output, expected)

    def test_parse_curl_with_request_kargs(self):
        output = uncurlx.parse(
            f"curl '{ENDPOINT}' -H 'Accept-Encoding: gzip,deflate,sdch'",
            timeout=0.1,
            allow_redirects=True,
        )
        expected = (
            """httpx.get("{}",""".format(ENDPOINT)
            + """
    allow_redirects=True,
    timeout=0.1,
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={},
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)
        output = uncurlx.parse(
            f"curl '{ENDPOINT}' -H 'Accept-Encoding: gzip,deflate,sdch'",
            timeout=0.1,
        )
        expected = (
            """httpx.get("{}",""".format(ENDPOINT)
            + """
    timeout=0.1,
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={},
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_parse_curl_with_escaped_newlines(self):
        output = uncurlx.parse(
            f"""curl '{ENDPOINT}' \\\n -H 'Accept-Encoding: gzip,deflate' \\\n --insecure"""
        )
        expected = (
            """httpx.get("{}",""".format(ENDPOINT)
            + """
    headers={
        "Accept-Encoding": "gzip,deflate"
    },
    cookies={},
    auth=(),
    proxy={},
    verify=False
)"""
        )
        self.assertEqual(output, expected)

    def test_parse_curl_escaped_unicode_in_cookie(self):
        output = uncurlx.parse(
            f"""curl '{ENDPOINT}' -H $'cookie: sid=00Dt00000004XYz\\u0021ARg' """
        )
        expected = (
            f"""httpx.get("{ENDPOINT}","""
            """
    headers={},
    cookies={
        "sid": "00Dt00000004XYz!ARg"
    },
    auth=(),
    proxy={},
)"""
        )
        self.assertEqual(output, expected)

    def test_parse_curl_with_proxy_and_proxy_auth(self):
        output = uncurlx.parse(f"curl '{ENDPOINT}' -U user: -x proxy.python.org:8080")
        expected = (
            """httpx.get("{}",""".format(ENDPOINT)
            + """
    headers={},
    cookies={},
    auth=(),
    proxy={'http': 'http://user:@proxy.python.org:8080/', 'https': 'http://user:@proxy.python.org:8080/'},
)"""
        )
        self.assertEqual(output, expected)

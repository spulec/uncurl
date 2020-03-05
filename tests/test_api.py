import sure  # Hey! Do not delete this import for the tests to pass

import uncurl


def test_basic_get():
    uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl'").should.equal(
        """requests.get("https://pypi.python.org/pypi/uncurl",
    headers={},
    cookies={},
)"""
    )


def test_colon_header():
    uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl' -H ':authority:mobile.twitter.com'").should.equal(
        """requests.get("https://pypi.python.org/pypi/uncurl",
    headers={
        ":authority": "mobile.twitter.com"
    },
    cookies={},
)"""
    )


def test_basic_headers():
    uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Accept-Language: en-US,en;q=0.8'").should.equal(
        """requests.get("https://pypi.python.org/pypi/uncurl",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "en-US,en;q=0.8"
    },
    cookies={},
)"""
    )


def test_cookies():
    uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'").should.equal(
        """requests.get("https://pypi.python.org/pypi/uncurl",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
    },
)"""
    )


def test_cookies_lowercase():
    uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'cookie: foo=bar; baz=baz2'").should.equal(
        """requests.get("https://pypi.python.org/pypi/uncurl",
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
    },
)"""
    )


def test_post():
    uncurl.parse("""curl 'https://pypi.python.org/pypi/uncurl' --data '[{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"},"now":1396219192277,"ab":{"welcome_email":{"v":"2","g":2}}}]' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'""").should.equal(
        """requests.post("https://pypi.python.org/pypi/uncurl",
    data='[{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"},"now":1396219192277,"ab":{"welcome_email":{"v":"2","g":2}}}]',
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
    },
)"""
    )


def test_post_with_dict_data():
    uncurl.parse("""curl 'https://pypi.python.org/pypi/uncurl' --data '{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"}}' -H 'Accept-Encoding: gzip,deflate,sdch' -H 'Cookie: foo=bar; baz=baz2'""").should.equal(
        """requests.post("https://pypi.python.org/pypi/uncurl",
    data='{"evt":"newsletter.show","properties":{"newsletter_type":"userprofile"}}',
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={
        "baz": "baz2",
        "foo": "bar"
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


def test_parse_curl_with_another_binary_data():
    uncurl.parse("""curl -H 'PID: 20000079' -H 'MT: 4' -H 'DivideVersion: 1.0' -H 'SupPhone: Redmi Note 3' -H 'SupFirm: 5.0.2' -H 'IMEI: wx_app' -H 'IMSI: wx_app' -H 'SessionId: ' -H 'CUID: wx_app' -H 'ProtocolVersion: 1.0' -H 'Sign: 7876480679c3cfe9ec0f82da290f0e0e' -H 'Accept: /' -H 'BodyEncryptType: 0' -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36 hap/1.0/oppo com.nearme.instant.platform/2.1.0beta1 com.felink.quickapp.reader/1.0.3 ({"packageName":"com.oppo.market","type":"other","extra":{}})' -H 'Content-Type: text/plain; charset=utf-8' -H 'Host: pandahomeios.ifjing.com' --data-binary '{"CateID":"508","PageIndex":1,"PageSize":30}' --compressed 'http://pandahomeios.ifjing.com/action.ashx/otheraction/9028'""").should.equals(
        r"""requests.post("http://pandahomeios.ifjing.com/action.ashx/otheraction/9028",
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
)""")


def test_parse_curl_with_insecure_flag():
    uncurl.parse("""curl 'https://pypi.python.org/pypi/uncurl' --insecure""").should.equal(
        """requests.get("https://pypi.python.org/pypi/uncurl",
    headers={},
    cookies={},
    verify=False
)"""
    )

def test_parse_curl_with_request_kargs():
    
    uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl' -H 'Accept-Encoding: gzip,deflate,sdch'", timeout=0.1, allow_redirects=True).should.equal("""requests.get("https://pypi.python.org/pypi/uncurl",
    allow_redirects=True,
    timeout=0.1,
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={},
)""")
                      
    uncurl.parse("curl 'https://pypi.python.org/pypi/uncurl' -H 'Accept-Encoding: gzip,deflate,sdch'", timeout=0.1).should.equal("""requests.get("https://pypi.python.org/pypi/uncurl",
    timeout=0.1,
    headers={
        "Accept-Encoding": "gzip,deflate,sdch"
    },
    cookies={},
)""")
                      


if __name__ == '__main__':
    test_basic_get()
    test_colon_header()
    test_basic_headers()
    test_cookies()
    test_cookies_lowercase()
    test_post()
    test_post_with_dict_data()
    test_post_with_string_data()
    test_parse_curl_with_binary_data()
    test_parse_curl_with_another_binary_data()
    test_parse_curl_with_insecure_flag()
    test_parse_curl_with_request_kargs()


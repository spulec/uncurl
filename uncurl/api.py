import argparse
import json
import re
import shlex
from collections import OrderedDict

from six.moves import http_cookies as Cookie

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('url')
parser.add_argument('-d', '--data')
parser.add_argument('-b', '--data-binary', default=None)
parser.add_argument('-X', default='')
parser.add_argument('-H', '--header', action='append', default=[])
parser.add_argument('--compressed', action='store_true')
parser.add_argument('--insecure', action='store_true')


def parse(curl_command):
    method = "get"

    tokens = shlex.split(curl_command)
    parsed_args = parser.parse_args(tokens)

    base_indent = " " * 4
    data_token = ''
    if parsed_args.X.lower() == 'post':
        method = 'post'
    post_data = parsed_args.data or parsed_args.data_binary
    if post_data:
        method = 'post'

        post_data = "'{}'".format(post_data)
        data_token = '{}data={},\n'.format(base_indent, post_data)

    cookie_dict = OrderedDict()
    quoted_headers = OrderedDict()

    for curl_header in parsed_args.header:
        if curl_header.startswith(':'):
            occurrence = [m.start() for m in re.finditer(':', curl_header)]
            header_key, header_value = curl_header[:occurrence[1]], curl_header[occurrence[1] + 1:]
        else:
            header_key, header_value = curl_header.split(":", 1)

        if header_key.lower() == 'cookie':
            cookie = Cookie.SimpleCookie(header_value)
            for key in cookie:
                cookie_dict[key] = cookie[key].value
        else:
            quoted_headers[header_key] = header_value.strip()

    result = """requests.{method}("{url}",
{data_token}{headers_token},
{cookies_token},{security_token}
)""".format(
        method=method,
        url=parsed_args.url,
        data_token=data_token,
        headers_token="{}headers={}".format(base_indent, dict_to_pretty_string(quoted_headers)),
        cookies_token="{}cookies={}".format(base_indent, dict_to_pretty_string(cookie_dict)),
        security_token="\n%sverify=False" % base_indent if parsed_args.insecure else ""
    )
    return result


def dict_to_pretty_string(the_dict, indent=4):
    if not the_dict:
        return "{}"

    return ("\n" + " " * indent).join(
        json.dumps(the_dict, sort_keys=True, indent=indent, separators=(',', ': ')).splitlines())

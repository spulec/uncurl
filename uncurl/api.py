import argparse
from collections import OrderedDict
import Cookie
import json
import shlex

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('url')
parser.add_argument('-d', '--data')
parser.add_argument('-H', '--header', action='append', default=[])
parser.add_argument('--compressed', action='store_true')


def parse(curl_command):
    method = "get"

    tokens = shlex.split(curl_command)
    parsed_args = parser.parse_args(tokens)

    data_token = ''
    post_data = parsed_args.data
    if post_data:
        method = 'post'
        try:
            post_data_json = json.loads(post_data)
        except ValueError:
            post_data_json = None

        # If we found JSON and it is a dict, pull it apart. Otherwise, just leave as a string
        if post_data_json and isinstance(post_data_json, dict):
            post_data = dict_to_pretty_string(post_data_json)
        else:
            post_data = "'{}',\n".format(post_data)

        data_token = 'data={}'.format(post_data)

    cookie_dict = OrderedDict()
    quoted_headers = OrderedDict()
    for curl_header in parsed_args.header:
        header_key, header_value = curl_header.split(":", 1)

        if header_key == 'Cookie':
            cookie = Cookie.SimpleCookie(header_value)
            for key in cookie:
                cookie_dict[key] = cookie[key].value
        else:
            quoted_headers[header_key] = header_value.strip()

    result = """requests.{method}("{url}",\n{data_token}{headers_token}{cookies_token})""".format(
        method=method,
        url=parsed_args.url,
        data_token=data_token,
        headers_token="headers={}".format(dict_to_pretty_string(quoted_headers)),
        cookies_token="cookies={}".format(dict_to_pretty_string(cookie_dict)),
    )
    return result


def dict_to_pretty_string(the_dict, indent=0):
    if not the_dict:
        return "{},\n"

    base_indent = " " * indent
    inner_indent = base_indent + " " * 4

    return_value = "{\n"
    sorted_keys = sorted(the_dict.keys())
    for key in sorted_keys:
        value = the_dict[key]
        if isinstance(value, dict):
            value = dict_to_pretty_string(value, indent=indent + 4)
        else:
            value = '"{}",\n'.format(value)
        return_value += inner_indent + '"{0}": {1}'.format(key, value)

    return_value += base_indent + '},\n'

    return return_value

# -*- coding: utf-8 -*-
import argparse
import json
import re
import shlex
from collections import OrderedDict, namedtuple
from http.cookies import SimpleCookie
from typing import Any, List, Mapping, Optional, Tuple, Union

parser = argparse.ArgumentParser()
parser.add_argument("command")
parser.add_argument("url", default=None)
parser.add_argument("-d", "--data")
parser.add_argument("-b", "--data-binary", "--data-raw", default=None)
parser.add_argument("-X", "--request", default="")
parser.add_argument("-H", "--header", action="append", default=[])
parser.add_argument("--compressed", action="store_true")
parser.add_argument("-k", "--insecure", action="store_true")
parser.add_argument("--user", "-u", default=())
parser.add_argument("-i", "--include", action="store_true")
parser.add_argument("-s", "--silent", action="store_true")
parser.add_argument("-x", "--proxy", default={})
parser.add_argument("-U", "--proxy-user", default="")
parser.add_argument("-F", "--form", action="append", default=[])
parser.add_argument("-e", "--referer", default="")
parser.add_argument("-r", "--range", default="")
parser.add_argument("--unix-socket", default="")
parser.add_argument("--json", default="")
parser.add_argument("--url", dest="explicit_url", default=None)
# parser.add_argument("--basic", action="store_true", nargs=0)


BASE_INDENT = " " * 4

ParsedContext = namedtuple(
    "ParsedContext",
    [
        "method",
        "url",
        "data",
        "headers",
        "cookies",
        "verify",
        "auth",
        "proxy",
        "unix_socket",
        "json",
    ],
)


def normalize_newlines(multiline_text: str) -> str:
    return multiline_text.replace(" \\\n", " ")


def more_than_one_of(*args: Any) -> bool:
    """
    Check if more than one of the arguments is set to True.
    """
    return sum(bool(arg) for arg in args) > 1


def parse_headers(
    headers: List[str],
    data_content_type: Optional[str],
    range: Optional[str],
    referer: Optional[str],
) -> Tuple[Mapping[str, str], Mapping[str, str]]:
    """
    Parse headers from the curl command and return a dictionary of headers and cookies.
    :param headers: List of headers from the curl command.
    :return: A tuple containing a dictionary of headers and a dictionary of cookies.
    """
    quoted_headers = OrderedDict()
    cookie_dict = OrderedDict()

    for curl_header in headers:
        if curl_header.startswith(":"):
            occurrence = [m.start() for m in re.finditer(":", curl_header)]
            header_key, header_value = (
                curl_header[: occurrence[1]],
                curl_header[occurrence[1] + 1 :],
            )
        else:
            header_key, header_value = curl_header.split(":", 1)

        if header_key.lower().strip("$") == "cookie":
            cookie = SimpleCookie(bytes(header_value, "ascii").decode("unicode-escape"))
            for key in cookie:
                cookie_dict[key] = cookie[key].value
        else:
            quoted_headers[header_key] = header_value.strip()
    if data_content_type and "Content-Type" not in quoted_headers:
        quoted_headers["Content-Type"] = data_content_type
    if range:
        range_header_value = parse_curl_range(range)
        quoted_headers["Range"] = range_header_value
    if referer:
        quoted_headers["Referer"] = referer
    return quoted_headers, cookie_dict


def parse_context(curl_command: Union[str, List[str]]) -> ParsedContext:
    """
    Parse a curl command and return a ParsedContext object.
    :param curl_command: The curl command to parse, either as a string or a list of strings.
    :return: A ParsedContext object containing the parsed information.
    """
    method = "get"
    if isinstance(curl_command, str):
        tokens = shlex.split(normalize_newlines(curl_command))
        parsed_args = parser.parse_args(tokens)
    else:
        parsed_args = parser.parse_args(curl_command)
    if more_than_one_of(
        parsed_args.data,
        parsed_args.data_binary,
        parsed_args.form,
        parsed_args.json,
    ):
        raise ValueError(
            "You can only use one kind of -d/--data, -b/--data-binary, or -F/--form options at a time."
        )
    data_content_type = None
    post_data = parsed_args.data or parsed_args.data_binary or parsed_args.form
    json_data = None
    if parsed_args.form:
        data_content_type = "multipart/form-data"
    # elif parsed_args.data_binary:
    #     pass
    elif parsed_args.data:
        data_content_type = "application/x-www-form-urlencoded"
    elif parsed_args.json:
        try:
            json_data = repr(json.loads(parsed_args.json))
        except json.JSONDecodeError as jde:
            raise ValueError(
                "Invalid JSON format. Please provide a valid JSON string.",
                parsed_args.json,
            ) from jde

    if post_data or json_data:
        method = "post"

    if parsed_args.request:
        method = parsed_args.request.lower()

    quoted_headers, cookie_dict = parse_headers(
        parsed_args.header,
        data_content_type,
        referer=parsed_args.referer,
        range=parsed_args.range,
    )

    # add auth
    user = parsed_args.user
    if parsed_args.user:
        user = tuple(user.split(":"))

    # add proxy and its authentication if it's available.
    proxies = parse_proxy(parsed_args.proxy, parsed_args.proxy_user)

    return ParsedContext(
        method=method,
        url=parsed_args.url or parsed_args.explicit_url,
        data=post_data,
        headers=quoted_headers,
        cookies=cookie_dict,
        verify=parsed_args.insecure,
        auth=user,
        proxy=proxies,
        unix_socket=parsed_args.unix_socket,
        json=json_data if parsed_args.json else None,
    )


def parse_proxy(proxy: Optional[str], proxy_user: Optional[str]) -> Mapping[str, str]:
    # add proxy and its authentication if it's available.
    proxies = proxy
    # proxy_auth = proxy_user
    if proxy and proxy_user:
        proxies = {
            "http": "http://{}@{}/".format(proxy_user, proxy),
            "https": "http://{}@{}/".format(proxy_user, proxy),
        }
    elif proxy:
        proxies = {
            "http": "http://{}/".format(proxy),
            "https": "http://{}/".format(proxy),
        }
    return proxies


def parse(curl_command: Union[str, List[str]], **kargs) -> str:
    parsed_context = parse_context(curl_command)
    client = "httpx"
    client_setup = ""
    if parsed_context.unix_socket:
        client = "client"
        client_setup = f'{client} = httpx.Client(transport=httpx.HttpTransport(uds="{parsed_context.unix_socket}"))\n'
    data_token = ""
    if parsed_context.data:
        data_token = "{}data='{}',\n".format(BASE_INDENT, parsed_context.data)
    if parsed_context.json:
        data_token = "{}json={},".format(BASE_INDENT, parsed_context.json)
    verify_token = ""
    if parsed_context.verify:
        verify_token = "\n{}verify=False".format(BASE_INDENT)

    requests_kargs = ""
    for k, v in sorted(kargs.items()):
        requests_kargs += "{}{}={},\n".format(BASE_INDENT, k, str(v))

    indent_count = 1
    indent = indent_count * BASE_INDENT
    # auth_data = f'{BASE_INDENT}auth={parsed_context.auth}'
    auth_data = "{}auth={}".format(indent, parsed_context.auth)
    proxy_data = "\n{}proxy={}".format(indent, parsed_context.proxy)
    formatter = {
        "client_setup": client_setup,
        "client": "httpx",
        "method": parsed_context.method,
        "url": parsed_context.url,
        "data_token": data_token,
        "headers_token": "{}headers={}".format(
            indent * indent_count, dict_to_pretty_string(parsed_context.headers)
        ),
        "cookies_token": "{}cookies={}".format(
            indent * indent_count, dict_to_pretty_string(parsed_context.cookies)
        ),
        "security_token": verify_token,
        "requests_kargs": requests_kargs,
        "auth": auth_data,
        "proxies": proxy_data,
    }

    return """{client_setup}{client}.{method}("{url}",
{requests_kargs}{data_token}{headers_token},
{cookies_token},
{auth},{proxies},{security_token}
)""".format(**formatter).strip()


def parse_curl_range(range_str: str) -> str:
    """
    Parse a range string from curl and convert it to a format suitable for HTTP requests.
    """
    # Example: "bytes=0-499", "0-1096", "-100", "99-"
    if "=" in range_str:
        unit, ranges = range_str.split("=", maxsplit=1)
    else:
        unit = "bytes"
        ranges = range_str
    formatted_ranges = ", ".join(r.strip() for r in ranges.split(","))
    return f"{unit}={formatted_ranges}"


def dict_to_pretty_string(the_dict: Mapping[str, Any], indent=4) -> str:
    if not the_dict:
        return "{}"

    return ("\n" + " " * indent).join(
        json.dumps(
            the_dict, sort_keys=True, indent=indent, separators=(",", ": ")
        ).splitlines()
    )

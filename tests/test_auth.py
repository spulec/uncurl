import ast

import pytest

import uncurl


@pytest.mark.parametrize('option', ['-u', '--user'])
@pytest.mark.parametrize('credentials, expected', [
    ('name:secret', ('name', 'secret')),
    ('name:', ('name', '')),
    ('name:pass:word', ('name', 'pass:word')),
    ('name::pass:', ('name', ':pass:')),
])
def test_auth_password_colons(option, credentials, expected):
    command = "curl https://example.com --cookie 'sample=true' {} '{}'".format(
        option, credentials
    )
    assert uncurl.parse_context(command).auth == expected

    call = ast.parse(uncurl.parse(command), mode='eval').body
    auth = next(
        keyword.value for keyword in call.keywords if keyword.arg == 'auth'
    )
    assert ast.literal_eval(auth) == expected

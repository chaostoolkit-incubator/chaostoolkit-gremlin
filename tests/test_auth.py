# -*- coding: utf-8 -*-
from chaoslib.exceptions import FailedActivity
import pytest
import requests
import requests_mock

from chaosgremlin import auth, auth_key, GREMLIN_BASE_URL

EMAIL = "jon@example.com"
PASSWORD = "notyourfatherluke"
ORG_NAME = "starpeace"
MOCK_KEY = 'examplekey'


def test_auth_fails():
    url = "{base}/users/auth".format(base=GREMLIN_BASE_URL)
    with requests_mock.mock() as m:
        m.post(
            url,
            text="Invalid credentials",
            status_code=403
        )

        with pytest.raises(FailedActivity) as ex:
            auth(EMAIL, PASSWORD, ORG_NAME)
        assert "Gremlin authentication failed: Invalid credentials" in str(ex)

def test_auth_key_none():
    url = "{base}/users/auth".format(base=GREMLIN_BASE_URL)
    with requests_mock.mock() as m:
        m.post(
            url,
            text="Invalid credentials",
            status_code=403
        )

        with pytest.raises(FailedActivity) as ex:
            auth_key(None)
        assert "Gremlin authentication failed: No API Key present" in str(ex)

def test_unknown_org():
    url = "{base}/users/auth".format(base=GREMLIN_BASE_URL)
    with requests_mock.mock() as m:
        m.post(
            url,
            json=[]
        )

        with pytest.raises(FailedActivity) as ex:
            auth(EMAIL, PASSWORD, ORG_NAME)
        assert "User '{u}' does not seem to belong to org '{o}'".format(
            u=EMAIL, o=ORG_NAME) in str(ex)

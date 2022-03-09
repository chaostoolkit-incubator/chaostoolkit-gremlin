# -*- coding: utf-8 -*-
import os
from unittest import mock
import uuid

from chaoslib.exceptions import FailedActivity
import pytest
import requests
import requests_mock

from chaosgremlin import GREMLIN_BASE_URL
from chaosgremlin.actions import attack

SECRETS = {
    "email": "jon@example.com",
    "password": "notyourfatherluke",
    "org_name": "starpeace"
}


def test_failed_creating_attack():
    auth_url = "{base}/users/auth".format(base=GREMLIN_BASE_URL)
    url = "{base}/attacks/new".format(base=GREMLIN_BASE_URL)
    with requests_mock.mock() as m:
        m.post(auth_url, json=[
            {
                'expires_at': '2099-10-10T18:30:19.360Z',
                'header': 'Bearer XYZ',
                'identifier': SECRETS["email"],
                'org_id': str(uuid.uuid4()),
                'org_name': SECRETS["org_name"],
                'renew_token': str(uuid.uuid4()),
                'role': 'SUPER',
                'teams': [{'identifier': 'mock_team_id'}],
                'token': str(uuid.uuid4())
            }
        ])
        m.post(url, status_code=400, text="invalid command")

        with pytest.raises(FailedActivity) as ex:
            attack(
                command={"type": "boom", "args": ["-i", "10.0.0.0/24"]},
                target={"type": "Exact", "exact": ["foo-server1"]},
                labels={"service": "foo-service"},
                secrets=SECRETS
            )
        assert "Gremlin attack failed: invalid command" in str(ex)

def test_failed_no_api_key():
    auth_url = "{base}/users/auth".format(base=GREMLIN_BASE_URL)
    url = "{base}/attacks/new".format(base=GREMLIN_BASE_URL)
    with requests_mock.mock() as m:
        m.post(auth_url, json=[
            {
                'expires_at': '2099-10-10T18:30:19.360Z',
                'header': 'Bearer XYZ',
                'identifier': SECRETS["email"],
                'org_id': str(uuid.uuid4()),
                'org_name': SECRETS["org_name"],
                'renew_token': str(uuid.uuid4()),
                'role': 'SUPER',
                'teams': [{'identifier': 'mock_team_id'}],
                'token': str(uuid.uuid4())
            }
        ])
        m.post(url, status_code=400, text="invalid command")

        with pytest.raises(FailedActivity) as ex:
            attack(
                command={"type": "boom", "args": ["-i", "10.0.0.0/24"]},
                target={"type": "Exact", "exact": ["foo-server1"]},
                labels={"service": "foo-service"}
            )
        assert "Gremlin attack failed: No API Key present" in str(ex)


def test_failed_no_team_id():
    auth_url = "{base}/users/auth".format(base=GREMLIN_BASE_URL)
    url = "{base}/attacks/new".format(base=GREMLIN_BASE_URL)
    with requests_mock.mock() as m:
        m.post(auth_url, json=[
            {
                'expires_at': '2099-10-10T18:30:19.360Z',
                'header': 'Bearer XYZ',
                'identifier': SECRETS["email"],
                'org_id': str(uuid.uuid4()),
                'org_name': SECRETS["org_name"],
                'renew_token': str(uuid.uuid4()),
                'role': 'SUPER',
                'teams': [{'identifier': 'mock_team_id'}],
                'token': str(uuid.uuid4())
            }
        ])
        m.post(url, status_code=400, text="invalid command")
        mock_api = mock.patch.dict(os.environ, {'GREMLIN_API_KEY': 'mock_key'})
        with pytest.raises(FailedActivity) as ex:
            mock_api.start()
            attack(
                command={"type": "boom", "args": ["-i", "10.0.0.0/24"]},
                target={"type": "Exact", "exact": ["foo-server1"]},
                labels={"service": "foo-service"}
            )
            mock_api.stop()
        assert "Gremlin attack failed: Team ID must be provided with API Key authentication." in str(ex)

# -*- coding: utf-8 -*-
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

# -*- coding: utf-8 -*-
import requests

from chaoslib.exceptions import FailedActivity

__all__ = ["__version__", "GREMLIN_BASE_URL", "auth"]

__version__ = '0.2.0'
GREMLIN_BASE_URL = "https://api.gremlininc.com/v1"


def auth(email: str, password: str, org_name: str):
    """
    Private function that authorizes against the Gremlin API.
    """
    url = "{base}/users/auth".format(base=GREMLIN_BASE_URL)
    r = requests.post(url, data={"email": email, "password": password})

    if r.status_code != 200:
        raise FailedActivity(
            "Gremlin authentication failed: {m}".format(m=r.text))

    session = None
    for info in r.json():
        if info["org_name"] == org_name:
            session = info
            break

    if not session:
        raise FailedActivity(
            "User '{u}' does not seem to belong to org '{o}'".format(
                u=email, o=org_name))

    return session

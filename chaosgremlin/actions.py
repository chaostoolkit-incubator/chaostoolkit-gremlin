# -*- coding: utf-8 -*-
from functools import wraps
import json
import os
from typing import Any, Dict

from logzero import logger
import requests

from chaoslib.exceptions import FailedActivity
from chaoslib.types import Secrets

from chaosgremlin import auth, auth_key, GREMLIN_BASE_URL


__all__ = ["attack"]


def attack(command: Dict[str, Any], target: Dict[str, Any],
           labels: Dict[str, Any] = None, tags: Dict[str, Any] = None,
           secrets: Secrets = None):
    """
    Send attack declaration (JSON) to Gremlin API for execution. Please refer to Gremlin's
    documentation for the meaning of each argument. The `secrets` argument is
    a mapping which must have the following keys: `email`, `password` and
    `org_name`.

    The function returns the identifier of the attack or raises
    :exc:`FailedActivity` if the authentication failed and
    when the attack could not be started.

    .. seealso:: https://www.gremlin.com/docs/
    """
    if secrets is not None:
        session = auth(**secrets)
    else:
        session = auth_key(os.environ.get('GREMLIN_API_KEY'))   # This change assumes that the API Key is declared as an environment variable  

    url = "{base}/attacks/new".format(base=GREMLIN_BASE_URL)
    r = requests.post(
        url,
        headers={
            "Authorization": session["header"]
        },
        json={
            "command": command,
            "target": target,
            "labels": labels,
            "tags": tags
        })

    if r.status_code != 201:
        raise FailedActivity(
            "Gremlin attack failed: {m}".format(m=r.text))

    result = r.text
    logger.debug("attack submitted successfully: {r}".format(r=result))

    return result

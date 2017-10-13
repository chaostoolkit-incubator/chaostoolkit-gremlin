# -*- coding: utf-8 -*-
from functools import wraps
import json
import os
from typing import Any, Dict

import requests

from chaoslib.exceptions import FailedAction
from chaoslib.types import Secrets

from chaosgremlin import auth, GREMLIN_BASE_URL


__all__ = ["attack"]


def attack(command: Dict[str, Any], target: Dict[str, Any],
           labels: Dict[str, Any] = None, tags: Dict[str, Any] = None,
           secrets: Secrets = None):
    """
    Triggers an attack on the CPU of a host. Please refer to Gremlin's
    documentation for the meaning of each argument. The `secrets` argument is
    a mapping which must have the following keys: `email`, `password` and
    `org_name`.

    The function returns the identifier of the attack or raises
    :exc:`FailedActivity` if the authentication failed and :exc:`FailedAction`
    when the attack could not be started.

    .. seealso:: https://app.gremlininc.com/docs/
    """
    session = auth(**secrets)

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
        raise FailedAction(
            "Gremlin attack failed: {m}".format(m=r.text))

    return r.text
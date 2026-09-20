"""HTTP Basic auth gate for the dashboard.

Set APP_USERNAME and APP_PASSWORD in the environment to enable. If either is
unset, the dashboard is publicly readable (intended for local development only).

This is NOT institutional SSO. Replace with OAuth/SAML before production rollout.
See DEPLOY.md for the institutional-pilot auth story.
"""
from __future__ import annotations

import os
from functools import wraps
from typing import Callable

from flask import Response, request


def is_enabled() -> bool:
    return bool(os.getenv("APP_USERNAME")) and bool(os.getenv("APP_PASSWORD"))


def requires_auth(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_enabled():
            return f(*args, **kwargs)

        auth = request.authorization
        if (
            auth is None
            or auth.username != os.getenv("APP_USERNAME")
            or auth.password != os.getenv("APP_PASSWORD")
        ):
            return Response(
                "Authentication required.",
                status=401,
                headers={"WWW-Authenticate": 'Basic realm="OULAD Dashboard"'},
            )
        return f(*args, **kwargs)

    return decorated

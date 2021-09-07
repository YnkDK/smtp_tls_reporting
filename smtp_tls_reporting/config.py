"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""

swagger_config = {
    'title': 'SMTP TLS reporting handler',
    'description': """
A number of protocols exist for establishing encrypted channels between SMTP Mail Transfer Agents (MTAs), including STARTTLS, DNS Based Authentication of Named Entities (DANE) TLSA, and MTA Strict Transport Security (MTA-STS). These protocols can fail due to misconfiguration or active attack, leading to undelivered messages or delivery over unencrypted or unauthenticated channels.

This service handles reports sent by any reporting organization. It implements the RFC 8460 reporting schema and handles the I-JSON either as plain text or encoded in gzip.
""",
    'termsOfService': None,
    'contact': {
        'name': 'Martin Storgaard Dieu',
        'email': 'martin@storgaarddieu.com'
    },
    'license': {
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT'
    },
    'version': '1.0',
    'uiversion': 3,
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'api',
            "route": '/api.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/api/"
}

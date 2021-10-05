"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
import datetime
import json
from typing import Any

from werkzeug.exceptions import NotFound

from smtp_tls_reporting.features.exceptions import InternalError, NotFoundError
from smtp_tls_reporting.features.exceptions._SmtpTlsReportingException import SmtpTlsReportingException


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        as_dict_attribute = getattr(o, "as_dict", None)
        if callable(as_dict_attribute):
            return o.as_dict()
        return json.JSONEncoder.default(self, o)


def setup_error_handler(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, NotFound):
            e = NotFoundError(e)

        if not isinstance(e, SmtpTlsReportingException):
            e = InternalError(e)

        return {
                   'error_code': e.error_code,
                   'error_message': e.error_message
               }, e.http_status

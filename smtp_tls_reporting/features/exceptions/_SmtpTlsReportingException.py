"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""


class SmtpTlsReportingException(Exception):
    def __init__(self, original_exception: Exception, error_code: str, error_message: str, http_status: int):
        self._original_exception = original_exception
        self._error_code = error_code
        self._error_message = error_message
        self._http_status = http_status

    @property
    def error_code(self) -> str:
        return self._error_code

    @property
    def error_message(self) -> str:
        return self._error_message

    @property
    def http_status(self) -> int:
        return self._http_status

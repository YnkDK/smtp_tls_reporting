"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
from smtp_tls_reporting.features.exceptions._SmtpTlsReportingException import SmtpTlsReportingException

ERROR_MESSAGE = 'An error occurred during encoding/decoding the content to/from Gzip.'
ERROR_CODE = '400-01'


class GzipError(SmtpTlsReportingException):
    def __init__(self, original_exception: Exception):
        super(GzipError, self).__init__(
            original_exception=original_exception,
            error_code=ERROR_CODE,
            error_message=ERROR_MESSAGE,
            http_status=400
        )

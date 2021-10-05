"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
from smtp_tls_reporting.features.exceptions._SmtpTlsReportingException import SmtpTlsReportingException

ERROR_MESSAGE = 'The server encountered an unexpected condition that prevented it from fulfilling the request.'
ERROR_CODE = '500-01'


class InternalError(SmtpTlsReportingException):
    def __init__(self, original_exception: Exception):
        super(InternalError, self).__init__(
            original_exception=original_exception,
            error_code=ERROR_CODE,
            error_message=ERROR_MESSAGE,
            http_status=500
        )

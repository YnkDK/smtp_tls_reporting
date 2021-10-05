"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
from smtp_tls_reporting.features.exceptions._SmtpTlsReportingException import SmtpTlsReportingException

ERROR_CODE = '404-01'
ERROR_MESSAGE = 'The requested resource could not be found but may be available in the future. ' \
                'Subsequent requests by the client are permissible.'


class NotFoundError(SmtpTlsReportingException):
    def __init__(self, original_exception: Exception):
        super(NotFoundError, self).__init__(
            original_exception=original_exception,
            error_code=ERROR_CODE,
            error_message=ERROR_MESSAGE,
            http_status=404
        )

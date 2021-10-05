"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
from smtp_tls_reporting.features.exceptions._SmtpTlsReportingException import SmtpTlsReportingException

ERROR_CODE = '400-03'
ERROR_MESSAGE = 'Missing required parameter: {:s}'


class MissingParameterError(SmtpTlsReportingException):
    def __init__(self, original_exception: AssertionError):
        assert isinstance(original_exception, AssertionError)
        assert len(original_exception.args) == 1
        assert isinstance(original_exception.args[0], str)
        message = original_exception.args[0]

        super(MissingParameterError, self).__init__(
            original_exception=original_exception,
            error_code=ERROR_CODE,
            error_message=ERROR_MESSAGE.format(message),
            http_status=400
        )

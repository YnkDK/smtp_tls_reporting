"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
import re
from unittest import TestCase

from smtp_tls_reporting.features.exceptions._SmtpTlsReportingException import SmtpTlsReportingException


class TestSmtpTlsReportingException(TestCase):
    _exceptions = frozenset()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        TestSmtpTlsReportingException._exceptions = frozenset(SmtpTlsReportingException.__subclasses__())

    def test_unique_error_codes(self):
        bogus_exception = AssertionError('unittest')
        error_codes = set()
        for custom_exception in TestSmtpTlsReportingException._exceptions:
            instance = custom_exception(bogus_exception)
            error_codes.add(instance.error_code)

        self.assertGreater(
            len(error_codes),
            0,
            'Did not find any classes inheriting {:s}'.format(SmtpTlsReportingException.__name__)
        )
        # If any duplicate error codes were found, only 1 of them will be in the set error_codes.
        # This means that if the number of elements within error_codes is the same as the set of all exceptions
        # there were no duplicates found.
        self.assertEqual(len(error_codes), len(TestSmtpTlsReportingException._exceptions))

    def test_error_code_is_formatted(self):
        bogus_exception = AssertionError('unittest')
        error_code_pattern = re.compile(r'^\d+-\d+$')
        for custom_exception in TestSmtpTlsReportingException._exceptions:
            instance = custom_exception(bogus_exception)
            http_status = str(instance.http_status)

            self.assertTrue(
                instance.error_code.startswith(http_status),
                '"{:s}" did not start with "{:s}" on instance of {:s}'.format(
                    instance.error_code,
                    http_status,
                    custom_exception.__name__
                )
            )
            self.assertTrue(error_code_pattern.match(instance.error_code), custom_exception.__name__)

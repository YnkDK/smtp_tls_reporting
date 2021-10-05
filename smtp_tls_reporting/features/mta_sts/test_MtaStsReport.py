"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
import datetime
import io

import werkzeug.datastructures
from parameterized import parameterized

from smtp_tls_reporting.features.exceptions import InternalError, JsonError, GzipError
from smtp_tls_reporting.features.mta_sts._MtaStsReport import MtaStsReport
from smtp_tls_reporting.features.mta_sts.test_assertion_example_report import TestAssertionExampleReport, \
    test_data_files_iterator


class TestMtaStsReport(TestAssertionExampleReport):
    def test_set_report(self):
        report = MtaStsReport()
        pangram = b'The quick brown fox jumps over the lazy dog'
        test_report = werkzeug.datastructures.FileStorage(stream=io.BytesIO(pangram))

        report.set_report(test_report)

    def test_set_report_error(self):
        exception_thrown = NotImplementedError()
        report = MtaStsReport()
        stream = io.BytesIO(b'The quick brown fox jumps over the lazy dog')
        stream.close()
        test_report = werkzeug.datastructures.FileStorage(stream=stream)

        try:
            report.set_report(test_report)
        except InternalError as e:
            exception_thrown = e

        self.assertIsInstance(exception_thrown, InternalError)

    def test_parse_error(self):
        exception_thrown = NotImplementedError()
        report = MtaStsReport()
        test_report = TestMtaStsReport.data_file_as_filestorage('date_error.json')
        report.set_report(test_report)

        try:
            report.parse()
        except JsonError as e:
            exception_thrown = e

        self.assertIsInstance(exception_thrown, JsonError)

    def test_parse_invalid_json(self):
        exception_thrown = NotImplementedError()
        report = MtaStsReport()
        pangram = b'{"invalid_json": "missing_bracket ->"'
        test_report = werkzeug.datastructures.FileStorage(stream=io.BytesIO(pangram))
        report.set_report(test_report)

        try:
            report.parse()
        except JsonError as e:
            exception_thrown = e

        self.assertIsInstance(exception_thrown, JsonError)

    def test_parse_invalid_gz(self):
        exception_thrown = NotImplementedError()
        report = MtaStsReport()
        test_report = werkzeug.datastructures.FileStorage(stream=io.BytesIO(MtaStsReport.MAGIC_BYTE_GZ))
        report.set_report(test_report)

        try:
            report.parse()
        except GzipError as e:
            exception_thrown = e

        self.assertIsInstance(exception_thrown, GzipError)

    @parameterized.expand(test_data_files_iterator)
    def test_parse(self, test_data_file: str):
        report = MtaStsReport()
        test_report = TestMtaStsReport.data_file_as_filestorage(test_data_file)
        report.set_report(test_report)

        report.parse()

        self.assert_example_report_parsed_correctly(report)

    def test_parse_no_policies(self):
        report = MtaStsReport()
        test_report = TestMtaStsReport.data_file_as_filestorage('no-policies.json')
        report.set_report(test_report)

        report.parse()

        self.assertEqual(0, len(report.policies))

    def test_as_dict(self):
        report = MtaStsReport()
        test_report = TestMtaStsReport.data_file_as_filestorage(next(test_data_files_iterator()))
        report.set_report(test_report)
        report.parse()

        report = report.as_dict()

        self.assertEqual(report, {
            'failures': ['A policy has failures. Total count: 303.'],
            'meta': {
                'organization_name': 'Company-X',
                'start': datetime.datetime(2016, 4, 1),
                'end': datetime.datetime(2016, 4, 1, 23, 59, 59),
                'contact_info': 'sts-reporting@company-x.example',
                'report_id': '5065427c-23d3-47ca-b6e0-946ea0e8c4be'
            },
            'policies': [{
                'policy_type': 'sts',
                'policy_string': [
                    'version: STSv1',
                    'mode: testing',
                    'mx: *.mail.company-y.example',
                    'max_age: 86400'
                ],
                'policy_domain': 'company-y.example',
                'mx_host': '*.mail.company-y.example',
                'total_successful_session_count': 5326,
                'total_failure_session_count': 303,
                'failure_details': [
                    {
                        'result_type': 'certificate-expired',
                        'sending_mta_ip': '2001:db8:abcd:0012::1',
                        'receiving_mx_hostname': 'mx1.mail.company-y.example',
                        'receiving_mx_helo': None,
                        'receiving_ip': None,
                        'failed_session_count': 100,
                        'additional_information': None,
                        'failure_error_code': None
                    },
                    {
                        'result_type': 'starttls-not-supported',
                        'sending_mta_ip': '2001:db8:abcd:0013::1',
                        'receiving_mx_hostname': 'mx2.mail.company-y.example',
                        'receiving_mx_helo': None,
                        'receiving_ip': '203.0.113.56',
                        'failed_session_count': 200,
                        'additional_information': 'https://reports.company-x.example/report_info?id=5065427c-23d3#StarttlsNotSupported',
                        'failure_error_code': None
                    },
                    {
                        'result_type': 'validation-failure',
                        'sending_mta_ip': '198.51.100.62',
                        'receiving_mx_hostname': 'mx-backup.mail.company-y.example',
                        'receiving_mx_helo': None,
                        'receiving_ip': '203.0.113.58',
                        'failed_session_count': 3,
                        'additional_information': None,
                        'failure_error_code': 'X509_V_ERR_PROXY_PATH_LENGTH_EXCEEDED'
                    }
                ]
            }]
        })

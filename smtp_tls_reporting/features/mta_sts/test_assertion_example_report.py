"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
import datetime
import io
import os
import unittest

import werkzeug.datastructures

from smtp_tls_reporting.features.mta_sts._FailureDetail import FailureDetail
from smtp_tls_reporting.features.mta_sts._MtaStsReport import MtaStsReport
from smtp_tls_reporting.features.mta_sts._Policy import Policy
from smtp_tls_reporting.features.mta_sts._ReportMeta import ReportMeta


def test_data_files_iterator():
    yield 'example.json'
    yield 'example.gz'


class TestAssertionExampleReport(unittest.TestCase):
    @staticmethod
    def data_file_as_filestorage(filename):
        with open(os.path.join('../../test_data/', filename), 'rb') as f:
            content = f.read()
        return werkzeug.datastructures.FileStorage(stream=io.BytesIO(content))

    def assert_example_report_parsed_correctly(self, report: MtaStsReport):
        self.assertFalse(report.has_empty_policy)
        self.assertEqual(1, len(report.all_failures()))
        self.assertEqual(303, report.total_failure_session_count)

        meta = report.meta
        self.assertIsInstance(meta, ReportMeta)
        self.assertEqual('Company-X', meta.organization_name)
        self.assertEqual(datetime.datetime(2016, 4, 1), meta.start)
        self.assertEqual(datetime.datetime(2016, 4, 1, 23, 59, 59), meta.end)
        self.assertEqual('sts-reporting@company-x.example', meta.contact_info)
        self.assertEqual('5065427c-23d3-47ca-b6e0-946ea0e8c4be', meta.report_id)

        self.assertEqual(1, len(report.policies))
        policy = report.policies[0]
        self.assertIsInstance(policy, Policy)
        self.assertEqual('sts', policy.policy_type)
        expected_policy_string = ['version: STSv1', 'mode: testing', 'mx: *.mail.company-y.example', 'max_age: 86400']
        self.assertListEqual(expected_policy_string, policy.policy_string)
        self.assertEqual('company-y.example', policy.policy_domain)
        self.assertEqual('*.mail.company-y.example', policy.mx_host)
        self.assertEqual(5326, policy.total_successful_session_count)
        self.assertEqual(303, policy.total_failure_session_count)

        self.assertEqual(3, len(policy.failure_details))

        detail = policy.failure_details[0]
        self.assertIsInstance(detail, FailureDetail)
        self.assertEqual('certificate-expired', detail.result_type)
        self.assertEqual('2001:db8:abcd:0012::1', detail.sending_mta_ip)
        self.assertEqual('mx1.mail.company-y.example', detail.receiving_mx_hostname)
        self.assertIsNone(detail.receiving_mx_helo)
        self.assertIsNone(detail.receiving_ip)
        self.assertEqual(100, detail.failed_session_count)
        self.assertIsNone(detail.additional_information)
        self.assertIsNone(detail.failure_error_code)

        detail = policy.failure_details[1]
        self.assertIsInstance(detail, FailureDetail)
        self.assertEqual('starttls-not-supported', detail.result_type)
        self.assertEqual('2001:db8:abcd:0013::1', detail.sending_mta_ip)
        self.assertEqual('mx2.mail.company-y.example', detail.receiving_mx_hostname)
        self.assertIsNone(detail.receiving_mx_helo)
        self.assertEqual('203.0.113.56', detail.receiving_ip)
        self.assertEqual(200, detail.failed_session_count)
        self.assertEqual(
            'https://reports.company-x.example/report_info?id=5065427c-23d3#StarttlsNotSupported',
            detail.additional_information)
        self.assertIsNone(detail.failure_error_code)

        detail = policy.failure_details[2]
        self.assertIsInstance(detail, FailureDetail)
        self.assertEqual('validation-failure', detail.result_type)
        self.assertEqual('198.51.100.62', detail.sending_mta_ip)
        self.assertEqual('mx-backup.mail.company-y.example', detail.receiving_mx_hostname)
        self.assertIsNone(detail.receiving_mx_helo)
        self.assertEqual('203.0.113.58', detail.receiving_ip)
        self.assertEqual(3, detail.failed_session_count)
        self.assertIsNone(detail.additional_information)
        self.assertEqual('X509_V_ERR_PROXY_PATH_LENGTH_EXCEEDED', detail.failure_error_code)

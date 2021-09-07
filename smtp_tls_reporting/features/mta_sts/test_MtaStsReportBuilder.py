"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
from smtp_tls_reporting.features.mta_sts.MtaStsReportBuilder import MtaStsReportBuilder
from smtp_tls_reporting.features.mta_sts.test_assertion_example_report import TestAssertionExampleReport, \
    test_data_files_iterator


class TestMtaStsReport(TestAssertionExampleReport):
    def test_builder(self):
        test_report = TestMtaStsReport.data_file_as_filestorage(next(test_data_files_iterator()))

        report = MtaStsReportBuilder.build_report(test_report)

        self.assert_example_report_parsed_correctly(report)

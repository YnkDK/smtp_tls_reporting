"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
import werkzeug.datastructures

from smtp_tls_reporting.features.mta_sts._MtaStsReport import MtaStsReport


class MtaStsReportBuilder:
    @staticmethod
    def build_report(report: werkzeug.datastructures.FileStorage) -> MtaStsReport:
        mta_sts_report = MtaStsReport()
        mta_sts_report.set_report(report)
        mta_sts_report.parse()
        return mta_sts_report

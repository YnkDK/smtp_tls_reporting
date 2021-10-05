"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
import gzip
import io
import json
from typing import List

import werkzeug.datastructures

from smtp_tls_reporting.features.exceptions import GzipError, InternalError, JsonError
from smtp_tls_reporting.features.mta_sts._Policy import Policy
from smtp_tls_reporting.features.mta_sts._ReportMeta import ReportMeta


class MtaStsReport:
    """The magic bytes for gz or tar.gz is 1f8b"""
    MAGIC_BYTE_GZ = b'\x1f\x8b'

    def __init__(self):
        self.__original_report = b''  # type: bytes
        self.__meta = ReportMeta()  # type: ReportMeta
        self.__policies = []  # type: List[Policy]
        self.__internal_exception = None  # type: Exception

    def set_report(self, report: werkzeug.datastructures.FileStorage):
        try:
            self.__original_report = report.stream.read()
        except Exception as e:
            raise InternalError(e)

    def parse(self):
        buffer = self.__original_report
        if buffer.startswith(MtaStsReport.MAGIC_BYTE_GZ):
            compressed_file = io.BytesIO(buffer)
            try:
                buffer = gzip.GzipFile(fileobj=compressed_file).read()
            except Exception as e:
                raise GzipError(e)

        try:
            raw_report = json.loads(buffer)
            self.__meta.build(raw_report)
            for policy in raw_report['policies']:
                self.__policies.append(Policy(policy))
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            raise JsonError(e)

    @property
    def total_failure_session_count(self) -> int:
        return sum(policy.total_failure_session_count for policy in self.__policies)

    @property
    def has_empty_policy(self) -> bool:
        return any(p.policy_string is None or p.policy_type == 'no-policy-found' for p in self.__policies)

    @property
    def meta(self) -> ReportMeta:
        return self.__meta

    @property
    def policies(self) -> List[Policy]:
        return self.__policies

    def all_failures(self) -> List[str]:
        failures = []
        total_failure_session_count = self.total_failure_session_count
        has_empty_policy = self.has_empty_policy

        if total_failure_session_count > 0:
            failures.append(f'A policy has failures. Total count: {total_failure_session_count}.')

        if has_empty_policy:
            failures.append('There is an empty policy.')

        return failures

    def as_dict(self):
        return {
            'failures': self.all_failures(),
            'meta': self.__meta.as_dict(),
            'policies': [p.as_dict() for p in self.__policies]
        }

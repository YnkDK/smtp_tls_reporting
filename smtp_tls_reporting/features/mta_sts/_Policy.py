"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
from smtp_tls_reporting.features.mta_sts._FailureDetail import FailureDetail


class Policy:
    def __init__(self, raw_policy: dict):
        meta = raw_policy['policy']
        summary = raw_policy['summary']

        self.policy_type = meta['policy-type']
        self.policy_string = meta.get('policy-string', None)
        self.policy_domain = meta['policy-domain']
        self.mx_host = meta.get('mx-host', None)
        self.total_successful_session_count = summary['total-successful-session-count']
        self.total_failure_session_count = summary['total-failure-session-count']
        self.failure_details = [FailureDetail(detail) for detail in raw_policy.get('failure-details', [])]

    def as_dict(self) -> dict:
        failure_details = [fd.as_dict() for fd in self.failure_details]
        policy = vars(self)
        policy['failure_details'] = failure_details
        return policy

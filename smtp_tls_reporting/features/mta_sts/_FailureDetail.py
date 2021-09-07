"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""


class FailureDetail:
    def __init__(self, raw_policy: dict):
        self.result_type = raw_policy.get('result-type')
        self.sending_mta_ip = raw_policy.get('sending-mta-ip')
        self.receiving_mx_hostname = raw_policy.get('receiving-mx-hostname')
        self.receiving_mx_helo = raw_policy.get('receiving-mx-helo', None)
        self.receiving_ip = raw_policy.get('receiving-ip', None)
        self.failed_session_count = int(raw_policy.get('failed-session-count'))
        self.additional_information = raw_policy.get('additional-information', None)
        self.failure_error_code = raw_policy.get('failure-error-code', None)

    def as_dict(self) -> dict:
        return vars(self)

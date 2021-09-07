"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
from flask import request, jsonify
from flask_restful import Resource
from werkzeug.datastructures import FileStorage

from smtp_tls_reporting.features.mta_sts.MtaStsReportBuilder import MtaStsReportBuilder


class MtaStsReports(Resource):
    @staticmethod
    def post():
        """Handles a new report
        The report is composed as a plaintext file encoded in the Internet JSON (I-JSON) format [RFC7493].

        Aggregate reports contain the following fields:
        1. Report metadata:
            - The organization responsible for the report
            - Contact information for one or more responsible parties for the contents of the report
            -  A unique identifier for the report
            -  The reporting date range for the report
        2. Policy, consisting of:
            - One of the following policy types:
                (1) the MTA-STS Policy applied (as a string),
                (2) the DANE TLSA record applied (as a string, with each RR entry of the RR set listed and separated by a semicolon),
                (3) the literal string "no-policy-found", if neither a DANE nor MTA-STS Policy could be found.
            - The domain for which the policy is applied
            - The MX host
        3. Aggregate counts, comprising result type, Sending MTA IP, receiving MTA hostname, session count, and an optional additional information field containing a URI for recipients to review further information on a failure type.

        Parses a new MTA-STS report in either plain text or encoded in gz format.
        ---
        consumes:
            - multipart/form-data
        parameters:
            - in: formData
              name: report
              type: file
              required: true
        responses:
            400:
                description: Indicates that the server cannot or will not process the request due to something that is perceived to be a client error
                schema:
                   id: BadRequest
                   properties:
                       error:
                           type: string
                           description: The error message to be understood by the client.
                           example: "Missing parameter: report"
            200:
                description: The parsed report
                schema:
                    id: MtaStsReport
                    properties:
                        failures:
                            type: array
                            description: Aggregated list of failures.
                            items:
                                type: string
                                example: "A policy has failures. Total count: 303."
                        meta:
                            type: object
                            description: Meta data about the report.
                            properties:
                                report_id:
                                    type: string
                                    example: "5065427c-23d3-47ca-b6e0-946ea0e8c4be"
                                organization_name:
                                    type: string
                                    example: "Company-X"
                                contact_info:
                                    type: string
                                    format: email
                                    example: "sts-reporting@company-x.example"
                                start:
                                    type: string
                                    format: date-time
                                    example: 2016-04-01T00:00:00
                                end:
                                    type: string
                                    format: date-time
                                    example: 2016-04-01T23:59:59
                        policies:
                            type: array
                            items:
                                type: object
                                properties:
                                    policy_type:
                                        type: string
                                        enum: [tlsa, sts, no-policy-found]
                                        example: sts
                                    policy_domain:
                                        type: string
                                        example: "company-y.example"
                                    policy_string:
                                        type: array
                                        example: ["version: STSv1","mode: testing","mx: *.mail.company-y.example","max_age: 86400"]
                                        items:
                                            type: string
                                    total_failure_session_count:
                                        type: integer
                                        example: 303
                                    total_successful_session_count:
                                        type: integer
                                        example: 5326
                                    failure_details:
                                        type: array
                                        items:
                                            type: object
                                            properties:
                                                additional_information:
                                                    type: string
                                                    example: "https://reports.company-x.example/report_info?id=5065427c-23d3#StarttlsNotSupported"
                                                failed_session_count:
                                                    type: integer
                                                    example: 100
                                                failure_reason_code:
                                                    type: string
                                                    example: The certificate has expired
                                                receiving_ip:
                                                    type: string
                                                    format: ip
                                                    example: 203.0.113.56
                                                receiving_mx_helo:
                                                    type: string
                                                    example: HELO company-y.example
                                                receiving_mx_hostname:
                                                    type: string
                                                    example: mx1.mail.company-y.example
                                                result_type:
                                                    type: string
                                                    example: certificate-expired
                                                sending_mta_ip:
                                                    type: string
                                                    format: ip
                                                    example: "2001:db8:abcd:0013::1"
        """
        report = request.files.get('report')  # type: FileStorage
        if report is None:
            return {'error': 'Missing parameter: report'}, 400

        mta_sts_report = MtaStsReportBuilder.build_report(report)

        if mta_sts_report.has_parsing_errors:
            return {'error': mta_sts_report.parsing_error_message}, 400
        return jsonify(mta_sts_report)

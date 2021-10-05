"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""

from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from smtp_tls_reporting.config import swagger_config
from smtp_tls_reporting.controllers import CustomJsonEncoder, setup_error_handler
from smtp_tls_reporting.controllers.mta_sts_reports import MtaStsReports

app = Flask(__name__)
app.json_encoder = CustomJsonEncoder
setup_error_handler(app)

api = Api(app)
swagger = Swagger(app, config=swagger_config)

api.add_resource(MtaStsReports, '/api/reports/mta-sts')

if __name__ == '__main__':
    app.run(debug=True)

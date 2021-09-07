"""
    SMTP TLS reporting handler
    Copyright (C) 2021  Martin Storgaard Dieu

    This code is licensed under MIT license (see LICENSE.md for details)
"""
import datetime
import json
from typing import Any


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime.datetime):
            return o.isoformat()

        as_dict_attribute = getattr(o, "as_dict", None)
        if callable(as_dict_attribute):
            return o.as_dict()
        return json.JSONEncoder.default(self, o)

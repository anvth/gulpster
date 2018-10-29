from datetime import datetime
import json


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


def serialize(event_dict):
    return json.dumps(event_dict, cls=DateTimeEncoder)


def deserialize(event):
    return json.loads(event)

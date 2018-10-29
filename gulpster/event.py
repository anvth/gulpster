import uuid
from datetime import datetime
from dateutil.tz import tzlocal


class Event(object):
	def __init__(self, eventType, payload=None):
		self.eventType = eventType
		self.payload = payload
		self.identifier = str(uuid.uuid1())
		self.occurrenceTime = datetime.now(tzlocal())

	def asDict(self):
		return {
			'eventType': self.eventType,
			'identifier': self.identifier,
			'occurrenceTime': self.occurrenceTime,
			'payload': self.payload
			}

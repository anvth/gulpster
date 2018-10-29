import pika
from gulpster.event import Event
from gulpster.utils import serialize

from .base import BasePublisher


class Publisher(BasePublisher):
	def __init__(self, url=None):
		super(Publisher, self).__init__()

	def connect(self):
		self._connection = pika.BlockingConnection(self.params)		
		self._channel = self._connection.channel()
		self._channel.exchange_declare(exchange=self.EXCHANGE, type=self.EXCHANGE_TYPE)

	def start_publishing(self):
		evt = Event("com.home.test", {})
		self._channel.basic_publish(exchange=self.EXCHANGE, routing_key=self.ROUTING_KEY, body=serialize(evt.asDict()))
		print(" [x] Message sent to consumer")
		self._connection.close()

	def run(self):
		self.connect()
		self.start_publishing()

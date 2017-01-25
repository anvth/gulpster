import os
import sys
import logging
import pika
from pika import adapters

from base import BaseConsumer


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)


class Consumer(BaseConsumer):
	def __init__(self):
		super(Consumer, self).__init__()

	def set_event_listener(self, listener):
		self._event_listener = listener


	def notify_listener(self, evt):
		if self._event_listener:
			try:
				self._event_listener.handle_event(deserialize(evt))
			except Exception as e:
				print e


	def connect(self):
		LOGGER.info('Connecting to %s', self.url)
		self._connection = adapters.BlockingConnection(self.params)
		

		self._channel = self._connection.channel() # start a channel

		# create a function which is called on incoming messages
		def callback(ch, method, properties, body):
  			self.notify_listener(body)

		#set up subscription on the queue
		self._channel.basic_consume(callback,
  			queue=self.QUEUEcd ,
  			no_ack=True)

		# start consuming (blocks)
		self._channel.start_consuming()
		self._connection.close()


	def run(self):
		self.connect()
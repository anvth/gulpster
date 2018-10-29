import sys
import logging
from pika import adapters


from .base import BasePublisher
from ..event import Event
from ..utils import serialize


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)


class Publisher(BasePublisher):
	def __init__(self):
		super(Publisher, self).__init__()
		self._stopping = False
		self._acked = 0
		self._nacked = 0
		self._message_number = 0
		self._deliveries = []

	def reconnect(self):
		if not self._closing:
			self._connection = self.connect()

	def on_connection_closed(self, connection, reply_code, reply_text):
		self._channel = None
		if self._closing:
			self._connection.ioloop.stop()
		else:
			LOGGER.warning('Connection closed, reopening in 5 seconds: (%s) %s', reply_code, reply_text)
			self._connection.add_timeout(5, self.reconnect)

	def add_on_connection_close_callback(self):
		LOGGER.info('Adding on connection close callback')
		self._connection.add_on_close_callback(self.on_connection_closed)

	def add_on_channel_close_callback(self):
		LOGGER.info('Adding channel close callback')
		self._channel.add_on_close_callback(self.on_channel_closed)

	def on_channel_closed(self, channel, reply_code, reply_text):
		LOGGER.warning('Channel %i was closed: (%s) %s', channel, reply_code, reply_text)
		self._connection.close()

	def on_channel_open(self, channel):
		LOGGER.info('Channel opened')
		self._channel = channel
		self.add_on_channel_close_callback()
		self.setup_exchange(self.EXCHANGE)

	def setup_exchange(self, exchange_name):
		LOGGER.info('Declaring exchange %s', exchange_name)
		self._channel.exchange_declare(self.on_exchange_declareok, exchange_name, self.EXCHANGE_TYPE)

	def open_channel(self):
		LOGGER.info('Creating a new channel')
		self._connection.channel(on_open_callback=self.on_channel_open)

	def on_connection_open(self, unused_connection):
		LOGGER.info('Connection opened')
		self.add_on_connection_close_callback()
		self.open_channel()

	def connect(self):
		LOGGER.info('Connecting to %s', self.url)
		return adapters.TornadoConnection(self.params, self.on_connection_open)

	def on_exchange_declareok(self, unused_frame):
		LOGGER.info('Exchange declared')
		self.start_publishing()

	def start_publishing(self):
		LOGGER.info('Issuing consumer related RPC commands')
		self.enable_delivery_confirmations()
		self.schedule_next_message()

	def enable_delivery_confirmations(self):
		LOGGER.info('Issuing Confirm.Select RPC command')
		self._channel.confirm_delivery(self.on_delivery_confirmation)

	def on_delivery_confirmation(self, method_frame):
		confirmation_type = method_frame.method.NAME.split('.')[1].lower()
		LOGGER.info('Received %s for delivery tag: %i', confirmation_type, method_frame.method.delivery_tag)

		if confirmation_type == 'ack':
			self._acked += 1
		elif confirmation_type == 'nack':
			self._nacked += 1

		self._deliveries.remove(method_frame.method.delivery_tag)
		LOGGER.info('Published %i messages, %i have yet to be confirmed, %i were acked and %i were nacked',
					self._message_number, len(self._deliveries),
					self._acked, self._nacked)

	def schedule_next_message(self):
		if self._stopping:
			return

		LOGGER.info('Scheduling next message for %0.1f seconds', self.PUBLISH_INTERVAL)
		self._connection.add_timeout(self.PUBLISH_INTERVAL, self.publish_message)

	def publish_message(self):
		if self._stopping:
			return

		evt = Event("com.home.test", {})
		self._channel.basic_publish(exchange=self.EXCHANGE, routing_key=self.ROUTING_KEY, body=serialize(evt.asDict()))
		self._message_number += 1
		self._deliveries.append(self._message_number)
		LOGGER.info("Message sent")
		self.schedule_next_message()

	def run(self):
		self._connection = self.connect()
		self._connection.ioloop.start()

	def stop(self):
		self._closing = True
		self._stopping = True
		self._connection.close()
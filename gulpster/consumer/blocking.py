import os
import sys
import logging
import pika
from pika import adapters

from gulpster.event import Event
from gulpster.utils import deserialize
from gulpster.config import read_config_file

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)


class Consumer(object):
	def __init__(self):
		self.config = read_config_file()
		self.connection = None
		self.channel = None
		self.closing = False
		self.consumer_tag = None
		self._event_listener = None

		self.url = 'amqp://' + self.config['username'] + \
		           ':' + self.config['password'] + \
		           '@' + self.config['host'] + \
		           self.config['virtual_host']
				
		self.queue = self.config['queue']
		self.params = pika.URLParameters(self.url)
		self.params.socket_timeout = 5


	def set_event_listener(self, listener):
		self._event_listener = listener


	def notify_listener(self, evt):
		if self._event_listener:
			try:
				self._event_listener.handle_event(deserialize(evt))
			except Exception as e:
				print e


	def add_on_connection_close_callback(self):
		LOGGER.info('Adding connection close callback')
		self.connection.add_on_close_callback(self.on_connection_closed)


	def on_connection_closed(self, connection, reply_code, reply_text):
		self.channel = None
		if self.closing:
			self.connection.ioloop.stop()
		else:
			LOGGER.warning('Connection closed, reopening in 5 seconds: (%s) %s', reply_code, reply_text)
			self.connection.add_timeout(5, self.reconnect)


	def reconnect(self):
		if not self._closing:
			self.connection = self.connect()


	def open_channel(self):
		LOGGER.info('Creating a new channel')
		self.channel = self.connection.channel(on_open_callback=self.on_channel_open)


	def add_on_channel_close_callback(self):
		LOGGER.info('Adding channel close callback')
		self.channel.add_on_close_callback(self.on_channel_closed)

    
	def on_channel_closed(self, channel, reply_code, reply_text):
		LOGGER.warning('Channel %i was closed: (%s) %s', channel, reply_code, reply_text)
		self.connection.close()

    
	def on_channel_open(self, channel):
		LOGGER.info('Channel opened')
		self.channel = channel
		self.add_on_channel_close_callback()
		self.setup_queue(self.queue)


	def setup_queue(self, queue_name):
		LOGGER.info('Declaring queue %s', queue_name)
		self.channel.queue_declare(queue_name)


	def on_connection_open(self):
		LOGGER.info('Connection opened')
		self.add_on_connection_close_callback()
		self.open_channel()


	def connect(self):
		LOGGER.info('Connecting to %s', self.url)
		self.connection = adapters.TornadoConnection(self.params, self.on_connection_open)
		

		# self.channel = self.connection.channel() # start a channel

		# create a function which is called on incoming messages
		def callback(ch, method, properties, body):
  			self.notify_listener(body)

		#set up subscription on the queue
		self.channel.basic_consume(callback,
  			queue=self.queue,
  			no_ack=True)

		# start consuming (blocks)
		self.channel.start_consuming()
		self.connection.close()


	def run(self):
		self.connect()

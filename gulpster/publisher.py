import pika
from event import Event
from utils import serialize
from config import read_config_file

class Publisher(object):

	def __init__(self, url=None):
		self.config = read_config_file()
		self.queue = self.config['queue']
		self.url = 'amqp://' + self.config['username'] + \
				   ':' + self.config['password'] + \
				   '@' + self.config['host'] + \
				   self.config['virtual_host']
		self.params = pika.URLParameters(self.url)
		self.params.socket_timeout = 5

		self.connection = None
		self.channel = None

	def connect(self):
		self.connection = pika.BlockingConnection(self.params)		
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue=self.queue)

	def start_publishing(self):
		evt = Event("com.home.test", {})
		self.channel.basic_publish(exchange='', routing_key=self.queue, body=serialize(evt.asDict()))
		print " [x] Message sent to consumer"
		self.connection.close()

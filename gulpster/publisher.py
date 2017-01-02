import pika
from event import Event
from utils import serialize


class Publisher(object):

	def __init__(self, url=None):
		self.url = 'amqp://fuxghddt:yyCgDMbcfLI_7fv5lf9GHoPpl6w6_QtU@buck.rmq.cloudamqp.com/fuxghddt'
		self.params = pika.URLParameters(self.url)
		self.params.socket_timeout = 5

		self.connection = None
		self.channel = None

	def connect(self):
		self.connection = pika.BlockingConnection(self.params)		
		self.channel = self.connection.channel()
		self.channel.queue_declare(queue='test')

	def start_publishing(self):
		evt = Event("com.home.test", {})
		self.channel.basic_publish(exchange='', routing_key='test', body=serialize(evt.asDict()))
		print " [x] Message sent to consumer"
		self.connection.close()

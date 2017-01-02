from event import Event
from utils import deserialize
import pika, os, logging, time

logging.basicConfig()


class Consumer(object):
        def __init__(self):
                self._event_listener = None


        def set_event_listener(self, listener):
                self._event_listener = listener


        def notify_listener(self, evt):
                if self._event_listener:
                        try:
                                self._event_listener.handle_event(deserialize(evt))
                        except Exception as e:
                                print e

	def connect(self):
		url = 'amqp://fuxghddt:yyCgDMbcfLI_7fv5lf9GHoPpl6w6_QtU@buck.rmq.cloudamqp.com/fuxghddt'
		params = pika.URLParameters(url)
		params.socket_timeout = 5
		connection = pika.BlockingConnection(params) # Connect to CloudAMQP
		channel = connection.channel() # start a channel

		# create a function which is called on incoming messages
		def callback(ch, method, properties, body):
  			self.notify_listener(body)

		#set up subscription on the queue
		channel.basic_consume(callback,
  			queue='test',
  			no_ack=True)

		# start consuming (blocks)
		channel.start_consuming()
		connection.close()

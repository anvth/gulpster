import pika, os, logging, json
from event import Event

logging.basicConfig()

url = 'amqp://fuxghddt:yyCgDMbcfLI_7fv5lf9GHoPpl6w6_QtU@buck.rmq.cloudamqp.com/fuxghddt'
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel
channel.queue_declare(queue='pdfprocess') # Declare a queue
# send a message

evt = Event("com.dreamworks.test", {})
channel.basic_publish(exchange='', routing_key='pdfprocess', body='message')
print " [x] Message sent to consumer"
connection.close()

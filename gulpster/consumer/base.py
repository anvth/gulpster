import sys
import pika
import logging


from gulpster.utils import deserialize
from gulpster.config import read_config_file


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format=LOG_FORMAT)
LOGGER = logging.getLogger(__name__)


class BaseConsumer(object):
    """This is a Base Consumer class that will initialize all the parameters
    needed to establish and maintain connection with RabbitMQ host.

    This class also provides methods to set an event listener and notify 
    one when a message arrives.

    """
    def __init__(self, amqp_url=None):
        self.config = read_config_file()
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._event_listener = None
        
        self.url = 'amqp://' + self.config['username'] + \
                   ':' + self.config['password'] + \
                   '@' + self.config['host'] + \
                   self.config['virtual_host']
        self.params = pika.URLParameters(self.url)
        self.params.socket_timeout = 5
        
        self.EXCHANGE = self.config['exchange']
        self.EXCHANGE_TYPE = self.config['exchange_type']
        self.QUEUE = self.config['queue']
        self.ROUTING_KEY = self.config['routing_key']

    def set_event_listener(self, listener):
        LOGGER.info('Setting event listener to %s', listener)
        self._event_listener = listener

    def notify_listener(self, evt, delivery_tag):
        if self._event_listener:
            try:
                self._event_listener.handle_event(deserialize(evt))
                LOGGER.info('%s handled', evt)
            except Exception as e:
                LOGGER.error(e)

            self.acknowledge_message(delivery_tag)

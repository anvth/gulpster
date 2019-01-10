import pika
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential
)

from gulpster.utils import serialize

from .base import BasePublisher


class Publisher(BasePublisher):
    def __init__(self, url=None):
        super(Publisher, self).__init__()

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=0.2, max=60)
    )
    def connect(self):
        self._connection = pika.BlockingConnection(self.params)
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange=self.EXCHANGE, exchange_type=self.EXCHANGE_TYPE)

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=0.2, max=30)
    )
    def start_publishing(self, evt):
        self._channel.basic_publish(exchange=self.EXCHANGE, routing_key=self.ROUTING_KEY, body=serialize(evt.asDict()))
        print(" [x] Message sent to consumer")
        self._connection.close()

    def run(self):
        self.connect()
        self.start_publishing()

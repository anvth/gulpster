import pika
from tenacity import (
    retry,
    retry_if_result,
    stop_after_attempt,
    wait_exponential
)

from gulpster.event import Event
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
        self._channel.exchange_declare(exchange=self.EXCHANGE, type=self.EXCHANGE_TYPE)

    @retry(
        retry=retry_if_result(lambda result: result is None),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=0.2, max=1)
    )
    def start_publishing(self):
        evt = Event("com.home.test", {})
        self._channel.basic_publish(exchange=self.EXCHANGE, routing_key=self.ROUTING_KEY, body=serialize(evt.asDict()))
        print(" [x] Message sent to consumer")
        self._connection.close()

    def run(self):
        self.connect()
        self.start_publishing()

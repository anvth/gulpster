from gulpster.consumer.ioloop import Consumer
from gulpster.agentbase import BaseEventHandler, BaseConsumerAgent
from gulpster.agentbase import event


class App(object):
    def main(self):
        event_handler = SimpleEventHandler()

        consumer = Consumer()

        agent = BaseConsumerAgent(event_handler, consumer)
        agent.run()

    def run(self):
        self.main()


class SimpleEventHandler(BaseEventHandler):
    @event("com.home.test")
    def print_test_event(self, evt):
        print("Print test event")
        if evt is not None:
            print(('=== {}'.format(evt)))

    @event("com.home.hello")
    def print_hello_event(self, evt):
        print("Print hello event")
        if evt is not None:
            print(('=== {}'.format(evt)))


if __name__ == '__main__':
    App().run()

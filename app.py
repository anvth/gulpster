from consumer import Consumer
from agentbase import BaseEventHandler, BaseConsumerAgent
from agentbase import event


class App(object):
        def main(self):
                event_handler = SimpleEventHandler()


                consumer = Consumer()


                agent = BaseConsumerAgent(event_handler, consumer)
                agent.run()


        def run(self):
                self.main()




class SimpleEventHandler(BaseEventHandler):
    @event(None)
    def print_event(self, evt):
        if evt is not None:
            print('=== {}'.format(evt))


App().run()

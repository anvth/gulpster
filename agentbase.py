from functools import wraps


class event(object):
        def __init__(self, event):
                self.event = event


        def __call__(self, func):
                @wraps(func)
                def wrap(inst, evt, *args, **kwargs):
                        if self.event is None:
                                func(inst, evt, *args, **kwargs)
                        else:
                                return None


                wrap._event = True
                return wrap


class EventMeta(type):
        def __init__(cls, name, bases, dict):
                if not hasattr(cls, '_registry'):
                        cls._registry = {'handlers': []}


                for member in dict.values():
                        if hasattr(member, '_event'):
                                cls._registry['handlers'].append(member)
		super(EventMeta, cls).__init__(name, bases, dict)


class BaseEventHandler(object):
        __metaclass__ = EventMeta
        _registry = {'handlers': []}


        def handle_event(self, evt, *args, **kwargs):
                for handler in self._registry['handlers']:
                        handler(self, evt, *args, **kwargs)




class BaseConsumerAgent(object):
        def __init__(self, event_handler, consumer):
                self.event_handler = event_handler
                self.consumer = consumer


        def handle_event(self, evt, *args, **kwargs):
                self.event_handler.handle_event(evt, *args, **kwargs)


        def run(self):
                self.consumer.set_event_listener(self)
                self.consumer.connect()

from functools import wraps


class event(object):
    def __init__(self, event):
        self.event = event

    def __call__(self, func):
        @wraps(func)
        def wrap(inst, evt, *args, **kwargs):
            if self.event is not None:
                func(inst, evt, *args, **kwargs)
            else:
                return None

        wrap._event = True
        wrap.event_name = self.event
        return wrap


class EventMeta(type):
    def __init__(cls, name, bases, dict):
        if not hasattr(cls, '_registry'):
                cls._registry = {'handlers': []}

        for member in list(dict.values()):
            if hasattr(member, '_event'):
                try:
                    handler_index = [handler[0] for handler in cls._registry['handlers']].index(member.event_name)
                except ValueError:
                    cls._registry['handlers'].append((member.event_name, [dict[member.__name__]]))
                else:
                    cls._registry['handlers'][handler_index][1].append(dict[member.__name__])

        super(EventMeta, cls).__init__(name, bases, dict)


class BaseEventHandler(object, metaclass=EventMeta):
    _registry = {'handlers': []}

    def handle_event(self, evt, *args, **kwargs):
        for handler in dict(self._registry['handlers'])[evt['eventType']]:
                handler(self, evt, *args, **kwargs)


class BaseConsumerAgent(object):
    def __init__(self, event_handler, consumer):
        self.event_handler = event_handler
        self.consumer = consumer

    def handle_event(self, evt, *args, **kwargs):
        self.event_handler.handle_event(evt, *args, **kwargs)

    def run(self):
        self.consumer.set_event_listener(self)
        self.consumer.run()

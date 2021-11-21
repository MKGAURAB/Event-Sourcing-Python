from typing import List
from .event import Event
import functools


def method_dispatch(func):
    dispatcher = functools.singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    functools.update_wrapper(wrapper, func)
    return wrapper


class Aggregate:
    def __init__(self):
        self._events = []

    @property
    def events(self) -> List[Event]:
        return self._events

    def clear_events(self):
        self._events = []

    @method_dispatch
    def apply(self, event: Event):
        raise ValueError('Unknown event!')

    def reconstruct_from_event(self, event: Event):
        self.apply(event)

    def record_event(self, event: Event):
        self.reconstruct_from_event(event)
        self.events.append(event)
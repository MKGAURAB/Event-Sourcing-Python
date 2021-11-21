from abc import ABC, ABCMeta, abstractmethod
import json
import copy


class EventEncoder(json.JSONEncoder):
    def default(self, o):
        encoded = copy.deepcopy(o.__dict__)
        del encoded['type']
        return encoded


class Event(ABC, metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, aggregate_id: str, occurred_at: str):
        self.type = self.__class__.__name__
        self.aggregate_id = aggregate_id
        self.occurred_at = occurred_at

    def encode(self):
        return EventEncoder().encode(self)
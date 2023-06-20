import abc
from dataclasses import dataclass


class Event:
    pass


@dataclass
class LoggingEvent(Event):
    msg: str

import logging
from abc import ABC
from typing import Any, Callable, Dict, List, Type

_logger = logging.getLogger(__name__)


class Command(ABC):
    pass


class Query(ABC):
    pass


class Event(ABC):
    pass


class HandlerNotImplementedError(Exception):
    pass


class HandlerAlreadyRegisteredError(Exception):
    pass


class MessageBus:
    def __init__(self) -> None:
        self._command_handlers: Dict[Type[Any], Callable] = {}
        self._query_handlers: Dict[Type[Any], Callable] = {}
        self._event_handlers: Dict[Type[Any], List[Callable]] = {}

    def register_handler(self, msg_type: Type[Any], handler: Callable) -> None:
        if issubclass(msg_type, Command):
            if msg_type in self._command_handlers:
                raise HandlerAlreadyRegisteredError(f'Handler already registered for command type {msg_type}')
            self._command_handlers[msg_type] = handler
        elif issubclass(msg_type, Query):
            if msg_type in self._query_handlers:
                raise HandlerAlreadyRegisteredError(f'Handler already registered for query type {msg_type}')
            self._query_handlers[msg_type] = handler
        elif issubclass(msg_type, Event):
            if msg_type not in self._event_handlers:
                self._event_handlers[msg_type] = []
            self._event_handlers[msg_type].append(handler)
        else:
            raise ValueError(f"Unknown message type: {msg_type}")

    def publish(self, msg: Any) -> Any:
        _logger.debug(f'Publishing message: {msg}')
        msg_type = type(msg)
        if isinstance(msg, Command):
            if msg_type not in self._command_handlers:
                raise HandlerNotImplementedError(f'No handler implemented for command type {msg_type}')
            return self._command_handlers[msg_type](msg)
        elif isinstance(msg, Query):
            if msg_type not in self._query_handlers:
                raise HandlerNotImplementedError(f'No handler implemented for query type {msg_type}')
            return self._query_handlers[msg_type](msg)
        elif isinstance(msg, Event):
            if msg_type in self._event_handlers:
                for handler in self._event_handlers[msg_type]:
                    handler(msg)
        else:
            raise TypeError(f"Unknown message type: {msg_type}")

    def can_handle(self, msg_type: Type[Any]) -> bool:
        if issubclass(msg_type, Command):
            return msg_type in self._command_handlers
        elif issubclass(msg_type, Query):
            return msg_type in self._query_handlers
        elif issubclass(msg_type, Event):
            return msg_type in self._event_handlers
        else:
            raise TypeError(f"Unknown message type: {msg_type}")

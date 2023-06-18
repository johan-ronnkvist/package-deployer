import logging
from typing import Union, Dict, Type, Callable, List

from pkgdeployer.domain import commands
from pkgdeployer.domain import events
from pkgdeployer.domain import queries

_logger = logging.getLogger(__name__)

Message = Union[commands.Command, queries.Query, events.Event]


class MessageBus:
    def __init__(self,
                 event_handlers: Dict[Type[events.Event], List[Callable[[events.Event], None]]],
                 command_handlers: Dict[Type[commands.Command], Callable[[commands.Command], None]],
                 query_handlers: Dict[Type[queries.Query], Callable[[queries.Query], None]]):
        self._event_handlers = event_handlers
        self._command_handlers = command_handlers
        self._query_handlers = query_handlers

    def handle(self, message: Message):
        if isinstance(message, commands.Command):
            self._handle_command(message)
        elif isinstance(message, events.Event):
            self._handle_event(message)
        else:
            raise TypeError(f"Unknown message type {message}")

    def _handle_command(self, command: commands.Command):
        _logger.debug(f"Handling command {command}")
        try:
            handler = self._command_handlers[type(command)]
            handler(command)
        except Exception:
            _logger.exception(f"Failed to handle command {command}")
            raise

    def _handle_event(self, event: events.Event):
        _logger.debug(f"Handling event {event}")
        for handler in self._event_handlers[type(event)]:
            try:
                _logger.debug(f"Handling event {event} with handler {handler}")
                handler(event)
            except Exception:
                _logger.exception(f"Failed to handle event {event}")
                raise

    def _handle_query(self, query: queries.Query):
        _logger.debug(f"Handling query {query}")
        try:
            handler = self._query_handlers[type(query)]
            return handler(query)
        except Exception:
            _logger.exception(f"Failed to handle query {query}")
            raise

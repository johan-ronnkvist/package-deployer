from dataclasses import dataclass
from unittest.mock import Mock

import pytest

from pkgdeployer.services.messaging import MessageBus, Command, Event, Query, HandlerNotImplementedError, \
    HandlerAlreadyRegisteredError

@dataclass(frozen=True)
class TestCommand(Command):
    pass


@dataclass(frozen=True)
class TestEvent(Event):
    pass


@dataclass(frozen=True)
class TestQuery(Query):
    pass


class TestMessageBus:
    @pytest.mark.parametrize("msg_type", [TestCommand, TestEvent, TestQuery])
    def test_can_handle_commands(self, msg_type):
        messagebus = MessageBus(Mock())
        assert not messagebus.can_handle(msg_type)
        messagebus.register_handler(msg_type, lambda x: None)
        assert messagebus.can_handle(msg_type)

    @pytest.mark.parametrize("msg_type", [TestCommand, TestEvent, TestQuery])
    def test_message_invokes_handler(self, msg_type):
        messagebus = MessageBus(Mock())
        handler = Mock()
        messagebus.register_handler(msg_type, handler)
        messagebus.publish(msg_type())
        handler.assert_called_once()

    def test_event_types_can_have_multiple_handlers(self):
        messagebus = MessageBus(Mock())
        handler1 = Mock()
        handler2 = Mock()
        messagebus.register_handler(TestEvent, handler1)
        messagebus.register_handler(TestEvent, handler2)
        messagebus.publish(TestEvent())
        handler1.assert_called_once_with(TestEvent())
        handler2.assert_called_once_with(TestEvent())

    def test_calling_handle_with_incorrect_type_raises(self):
        messagebus = MessageBus(Mock())
        with pytest.raises(TypeError):
            messagebus.publish("test")

    def test_calling_register_handler_with_incorrect_type_raises(self):
        messagebus = MessageBus(Mock())
        with pytest.raises(TypeError):
            messagebus.register_handler("test", lambda x: None)

    @pytest.mark.parametrize("msg_type", [TestCommand, TestQuery])
    def test_calling_register_handler_with_already_registered_type_raises(self, msg_type):
        messagebus = MessageBus(Mock())
        messagebus.register_handler(msg_type, lambda x: None)
        with pytest.raises(HandlerAlreadyRegisteredError):
            messagebus.register_handler(msg_type, lambda x: None)

    @pytest.mark.parametrize("msg_type", [TestCommand, TestQuery])
    def test_calling_handle_with_unregistered_type_raises(self, msg_type):
        messagebus = MessageBus(Mock())
        with pytest.raises(HandlerNotImplementedError):
            messagebus.publish(msg_type())

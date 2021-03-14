from __future__ import absolute_import, division, print_function
__metaclass__ = type

from abc import abstractmethod
from enum import Enum


class XmlCommandType(Enum):
    CHANGE = 'change'
    REMOVE = 'remove'
    COUNT = 'count'
    EMPTY = 'empty'


class XmlCommand:
    def __init__(self, command_type: XmlCommandType, xpath, value=None):
        self._type = command_type
        self._xpath = xpath
        self._value = value if value is None else f'{value}'

    @property
    @abstractmethod
    def args(self) -> dict:
        raise NotImplementedError()

    @property
    def type(self):
        return self._type


class AddOrUpdateXmlCommand(XmlCommand):
    def __init__(self, xpath, value=None):
        super().__init__(XmlCommandType.CHANGE, xpath, value)

    @property
    def args(self) -> dict:
        return dict(
            xpath=self._xpath,
            value=self._value,
            pretty_print=True
        )


class AddEmptyXmlCommand(XmlCommand):
    def __init__(self, xpath):
        super().__init__(XmlCommandType.EMPTY, xpath)

    @property
    def args(self) -> dict:
        return dict(
            xpath=self._xpath,
            pretty_print=True
        )


class RemoveXmlCommand(XmlCommand):
    def __init__(self, xpath):
        super().__init__(XmlCommandType.REMOVE, xpath)

    @property
    def args(self) -> dict:
        return dict(
            xpath=self._xpath,
            state='absent',
            pretty_print=True
        )


class CountConditionalXmlCommand(XmlCommand):
    def __init__(self, xpath, check, then_commands=None, else_commands=None):
        super().__init__(XmlCommandType.COUNT, xpath)
        self._then_commands = then_commands if then_commands else []
        self._else_commands = else_commands if else_commands else []
        self._check = check

    @property
    def args(self) -> dict:
        return dict(
            xpath=self._xpath,
            count='yes'
        )

    def next_commands(self, count):
        return self._then_commands if self._check(count) else self._else_commands

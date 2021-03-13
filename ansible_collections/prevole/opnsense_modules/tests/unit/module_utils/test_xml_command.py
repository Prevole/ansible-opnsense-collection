from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command \
    import XmlCommand, AddOrUpdateXmlCommand, AddEmptyXmlCommand, RemoveXmlCommand, CountConditionalCommand, \
    XmlCommandType


class TestXmlCommand:
    def test_properties(self):
        command = XmlCommand(
            command_type=XmlCommandType.CHANGE,
            xpath='xpath'
        )

        assert command.type is XmlCommandType.CHANGE
        with pytest.raises(NotImplementedError):
            command.args


class TestAddOrUpdateXmlCommand:
    def test_args(self):
        command = AddOrUpdateXmlCommand(
            xpath='xpath',
            value='value'
        )

        assert command.type is XmlCommandType.CHANGE
        assert command.args == dict(
            xpath='xpath',
            value='value',
            pretty_print=True
        )


class TestAddEmptyXmlCommand:
    def test_args(self):
        command = AddEmptyXmlCommand(xpath='xpath')

        assert command.type is XmlCommandType.EMPTY
        assert command.args == dict(
            xpath='xpath',
            pretty_print=True
        )


class TestRemoveXmlCommand:
    def test_args(self):
        command = RemoveXmlCommand(xpath='xpath')

        assert command.type is XmlCommandType.REMOVE
        assert command.args == dict(
            xpath='xpath',
            state='absent',
            pretty_print=True
        )


class TestCountConditionalCommand:
    def test_args(self):
        command = CountConditionalCommand(
            xpath='xpath',
            check=lambda count: count == 0
        )

        assert command.type is XmlCommandType.COUNT
        assert command.args == dict(
            xpath='xpath',
            count='yes'
        )

    def test_next_commands(self):
        command = CountConditionalCommand(
            xpath='xpath',
            check=lambda count: count == 0
        )

        assert command.next_commands(0) == []
        assert command.next_commands(1) == []

        command = CountConditionalCommand(
            xpath='xpath',
            check=lambda count: count == 0,
            then_commands=[AddEmptyXmlCommand(xpath='xpath')],
            else_commands=[RemoveXmlCommand(xpath='xpath')]
        )

        assert len(command.next_commands(0)) is 1
        assert command.next_commands(0)[0].type is XmlCommandType.EMPTY

        assert len(command.next_commands(1)) is 1
        assert command.next_commands(1)[0].type is XmlCommandType.REMOVE

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command \
    import XmlCommand, AddOrUpdateXmlCommand, AddEmptyXmlCommand, RemoveXmlCommand, CountConditionalCommand


class TestXmlCommand:
    def test_properties(self):
        command = XmlCommand(
            command_type='test',
            path='path',
            xpath='xpath'
        )

        assert command.type is 'test'
        assert command.args is None


class TestAddOrUpdateXmlCommand:
    def test_args(self):
        command = AddOrUpdateXmlCommand(
            path='path',
            xpath='xpath',
            value='value'
        )

        assert command.type is 'change'
        assert command.args == dict(
            path='path',
            xpath='xpath',
            value='value',
            pretty_print=True
        )


class TestAddEmptyXmlCommand:
    def test_args(self):
        command = AddEmptyXmlCommand(
            path='path',
            xpath='xpath'
        )

        assert command.type is 'empty'
        assert command.args == dict(
            path='path',
            xpath='xpath',
            pretty_print=True
        )


class TestRemoveXmlCommand:
    def test_args(self):
        command = RemoveXmlCommand(
            path='path',
            xpath='xpath'
        )

        assert command.type is 'remove'
        assert command.args == dict(
            path='path',
            xpath='xpath',
            state='absent',
            pretty_print=True
        )


class TestCountConditionalCommand:
    def test_args(self):
        command = CountConditionalCommand(
            path='path',
            xpath='xpath',
            check=lambda count: count == 0
        )

        assert command.type is 'count'
        assert command.args == dict(
            path='path',
            xpath='xpath',
            count='yes'
        )

    def test_next_commands(self):
        command = CountConditionalCommand(
            path='path',
            xpath='xpath',
            check=lambda count: count == 0
        )

        assert command.next_commands(0) == []
        assert command.next_commands(1) == []

        command = CountConditionalCommand(
            path='path',
            xpath='xpath',
            check=lambda count: count == 0,
            then_commands=[AddEmptyXmlCommand(
                path='path',
                xpath='xpath'
            )],
            else_commands=[RemoveXmlCommand(
                path='path',
                xpath='xpath'
            )]
        )

        assert len(command.next_commands(0)) is 1
        assert command.next_commands(0)[0].type is 'empty'

        assert len(command.next_commands(1)) is 1
        assert command.next_commands(1)[0].type is 'remove'

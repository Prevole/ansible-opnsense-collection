from __future__ import absolute_import, division, print_function
__metaclass__ = type

COMMAND_TYPE_CHANGE = 'change'
COMMAND_TYPE_REMOVE = 'remove'
COMMAND_TYPE_COUNT = 'count'
COMMAND_TYPE_EMPTY = 'empty'


class XmlCommand:
    def __init__(self, command_type, path, xpath, value=None):
        self._type = command_type
        self._path = path
        self._xpath = xpath
        self._value = value if value is None else f'{value}'

    @property
    def args(self):
        pass

    @property
    def type(self):
        return self._type


class AddOrUpdateXmlCommand(XmlCommand):
    def __init__(self, path, xpath, value=None):
        super().__init__(COMMAND_TYPE_CHANGE, path, xpath, value)

    @property
    def args(self):
        return dict(
            path=self._path,
            xpath=self._xpath,
            value=self._value,
            pretty_print=True
        )


class AddEmptyXmlCommand(XmlCommand):
    def __init__(self, path, xpath):
        super().__init__(COMMAND_TYPE_EMPTY, path, xpath)

    @property
    def args(self):
        return dict(
            path=self._path,
            xpath=self._xpath,
            pretty_print=True
        )


class RemoveXmlCommand(XmlCommand):
    def __init__(self, path, xpath):
        super().__init__(COMMAND_TYPE_REMOVE, path, xpath)

    @property
    def args(self):
        return dict(
            path=self._path,
            xpath=self._xpath,
            state='absent',
            pretty_print=True
        )


class CountConditionalCommand(XmlCommand):
    def __init__(self, path, xpath, check, then_commands=None, else_commands=None):
        super().__init__(COMMAND_TYPE_COUNT, path, xpath)
        self._then_commands = then_commands if then_commands else []
        self._else_commands = else_commands if else_commands else []
        self._check = check

    @property
    def args(self):
        return dict(
            path=self._path,
            xpath=self._xpath,
            count='yes'
        )

    def next_commands(self, count):
        return self._then_commands if self._check(count) else self._else_commands

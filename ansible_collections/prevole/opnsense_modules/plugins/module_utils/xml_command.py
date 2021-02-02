from __future__ import absolute_import, division, print_function
__metaclass__ = type

COMMAND_TYPE_CHANGE = 'change'
COMMAND_TYPE_REMOVE = 'remove'


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

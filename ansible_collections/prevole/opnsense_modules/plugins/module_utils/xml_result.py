from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command \
    import COMMAND_TYPE_CHANGE, COMMAND_TYPE_REMOVE, COMMAND_TYPE_EMPTY, COMMAND_TYPE_COUNT

DEFAULT_TYPES = [
    COMMAND_TYPE_REMOVE,
    COMMAND_TYPE_EMPTY,
    COMMAND_TYPE_COUNT
]


class XmlResult(object):
    def __init__(self):
        self._changed = False
        self._failed = False
        self._msg = None
        self._exception = None
        self._operations = []

    def add(self, result, command):
        if result.get('changed', False) and not self._failed:
            self._changed = True
            self._build_details(result, command)

        elif result.get('failed', False):
            self._changed = False
            self._failed = True
            self._msg = result.get('msg', None)
            self._exception = result.get('exception', None)
            self._build_details(result, command)

    @property
    def operations(self):
        return self._operations

    @property
    def has_changed(self):
        return self._changed

    @property
    def has_failed(self):
        return self._failed

    @property
    def msg(self):
        return self._msg

    @property
    def exception(self):
        return self._exception

    def _build_details(self, result, command):
        xml = result.get('invocation', dict()).get('module_args', dict())

        if command.type == COMMAND_TYPE_CHANGE:
            self._operations.append({
                'value': xml.get('value'),
                f'{command.type}': xml.get('xpath')
            })
        elif command.type in DEFAULT_TYPES:
            self._operations.append({
                f'{command.type}': xml.get('xpath')
            })

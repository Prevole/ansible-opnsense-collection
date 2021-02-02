from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command \
    import COMMAND_TYPE_CHANGE


class XmlResult(object):
    def __init__(self):
        self._changed = False
        self._operations = []

    def add(self, result, command):
        if result.get('changed', False):
            self._changed = True

            xml = result.get('invocation', dict()).get('module_args', dict())

            if command.type == COMMAND_TYPE_CHANGE:
                self._operations.append({
                    'value': xml.get('value'),
                    f'{command.type}': xml.get('xpath')
                })
            else:
                self._operations.append({
                    f'{command.type}': xml.get('xpath')
                })

    def operations(self):
        return self._operations

    def has_changed(self):
        return self._changed

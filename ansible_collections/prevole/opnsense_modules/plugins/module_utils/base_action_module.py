from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.plugins.action import ActionBase

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_result import XmlResult


class BaseActionModule(ActionBase):
    def __init__(self, task, connection, play_context, loader, templar, shared_loader_obj):
        super().__init__(task, connection, play_context, loader, templar, shared_loader_obj)
        self.xml_result = XmlResult()

    def _run_commands(self, result, commands, task_vars):
        for command in commands:
            self.xml_result.add(self._execute_module(
                module_name='xml',
                module_args=command.args,
                task_vars=task_vars
            ), command)

        result.update(dict(xml=self.xml_result.operations()))
        result.update(dict(changed=self.xml_result.has_changed()))

        return result

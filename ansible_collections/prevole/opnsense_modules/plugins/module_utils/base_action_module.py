from __future__ import absolute_import, division, print_function
__metaclass__ = type

from abc import abstractmethod

from ansible.plugins.action import ActionBase

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command \
    import XmlCommandType, XmlCommand
from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_result \
    import XmlResult


class BaseActionModule(ActionBase):
    def __init__(self, task, connection, play_context, loader, templar, shared_loader_obj):
        super().__init__(task, connection, play_context, loader, templar, shared_loader_obj)
        self._xml_result = XmlResult()
        self._result = None

    def run(self, tmp=None, task_vars=None):
        self._result = super(BaseActionModule, self).run(tmp, task_vars)

        self._result.update(dict(sub_invocations=[]))

        self._result.update(self._execute_module(
            module_name=self.module_name,
            module_args=self._task.args,
            task_vars=task_vars
        ))

        self._run(task_vars)

        return self._result

    @property
    @abstractmethod
    def module_name(self):
        raise NotImplementedError()

    @abstractmethod
    def _run(self, task_vars):
        raise NotImplementedError()

    def _run_commands(self, commands: [XmlCommand], task_vars):
        for command in commands:
            if self._xml_result.has_failed:
                break

            try:
                args = command.args.copy()
                args.update(dict(path=self._task.args.get('path')))

                result = self._execute_module(
                    module_name='community.general.xml',
                    module_args=args,
                    task_vars=task_vars
                )

                if command.type == XmlCommandType.COUNT:
                    self._run_commands(command.next_commands(result.get('count')), task_vars)

                else:
                    self._xml_result.add(result, command)

            except Exception as e:
                self._result.update(dict(
                    failed=True,
                    msg='Something went wrong',
                    exception=e
                ))
                break

        self._result.update(dict(
            xml=self._xml_result.operations,
            changed=self._xml_result.has_changed,
            failed=self._xml_result.has_failed,
            msg=self._xml_result.msg,
            exception=self._xml_result.exception
        ))

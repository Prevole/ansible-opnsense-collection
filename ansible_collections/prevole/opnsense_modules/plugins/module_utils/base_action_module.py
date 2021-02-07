from __future__ import absolute_import, division, print_function
__metaclass__ = type

from abc import abstractmethod

from ansible.plugins.action import ActionBase

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command \
    import COMMAND_TYPE_COUNT
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
        pass

    @abstractmethod
    def _run(self, task_vars):
        pass

    def _run_commands(self, commands, task_vars):
        for command in commands:
            if not self._xml_result.has_failed:
                try:
                    result = self._execute_module(
                        module_name='xml',
                        module_args=command.args,
                        task_vars=task_vars
                    )

                    if command.type == COMMAND_TYPE_COUNT:
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

    # def _run_module(self, module_name, task_vars, args, error_msg):
    #     try:
    #         result = self._execute_module(
    #             module_name=module_name,
    #             module_args=args.copy(),
    #             task_vars=task_vars
    #         )
    #
    #         self._handle_result(result, msg=error_msg, module_name=module_name)
    #
    #         return result
    #
    #     except Exception as e:
    #         self._handle_result(
    #             dict(failed=True),
    #             msg=error_msg,
    #             exception=e,
    #             module_name=module_name
    #         )

    # def _handle_result(self, result, msg=None, exception=None, module_name=None):
    #     if module_name:
    #         result.update(dict(module=module_name))
    #
    #     self._result.get('sub_invocations').append(result)
    #
    #     self._result.update(dict(
    #         changed=result.get('changed', False),
    #         failed=result.get('failed', False)
    #     ))
    #
    #     if msg is not None:
    #         self._result.update(dict(msg=f'{msg} - {result.get("msg", "")}'))
    #
    #     if exception is not None:
    #         self._result.update(dict(exception=exception))

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from abc import abstractmethod
from uuid import uuid4

from ansible.plugins.action import ActionBase
from ansible.plugins.connection.local import Connection

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_result import XmlResult


class BaseActionModule(ActionBase):
    def __init__(self, task, connection, play_context, loader, templar, shared_loader_obj):
        super().__init__(task, connection, play_context, loader, templar, shared_loader_obj)
        self._xml_result = XmlResult()
        self._result = None
        self._path = None
        self._mode = 'remote'

    def run(self, tmp=None, task_vars=None):
        self._result = super(BaseActionModule, self).run(tmp, task_vars)

        self._result.update(dict(sub_invocations=[]))

        self._path = f'/tmp/{uuid4()}.xml'

        self._result.update(self._execute_module(
            module_name=self.module_name,
            module_args=self._task.args,
            task_vars=task_vars
        ))

        self._mode = self._task.args.get('mode')

        self._pre_run(task_vars)

        if not self._result.get('failed', False):
            self._run(task_vars)

        if not self._result.get('failed', False):
            self._post_run(task_vars)

        return self._result

    @property
    @abstractmethod
    def module_name(self):
        pass

    @abstractmethod
    def _run(self, task_vars):
        pass

    def _pre_run(self, task_vars):
        if self._is_remote():
            return

        self._run_action(
            action_name='fetch',
            task_vars=task_vars,
            args=dict(
                src=self._task.args.get('path'),
                dest=self._path,
                flat=True
            ),
            error_msg=f'Unable to fetch the configuration file {self._task.args.get("path")}'
        )

    def _post_run(self, task_vars):
        if self._is_remote():
            return

        result = self._run_module(
            module_name='stat',
            task_vars=task_vars,
            args=dict(
                path=self._task.args.get('path')
            ),
            error_msg=f'Unable to stat the configuration file {self._task.args.get("path")}'
        )

        self._run_action(
            action_name='copy',
            task_vars=task_vars,
            args=dict(
                src=self._path,
                dest=self._task.args.get('path'),
                mode=result.get('mode'),
                owner=result.get('pw_name'),
                group=result.get('gr_name')
            ),
            error_msg=f'Unable to copy the configuration file {self._task.args.get("path")}'
        )

    def _run_commands(self, commands, task_vars):
        if self._is_fetch():
            current_connection = self._connection

            self._connection = Connection(
                play_context=self._play_context,
                new_stdin=current_connection._new_stdin,
            )

        for command in commands:
            if not self._xml_result.has_failed:
                try:
                    result = self._execute_module(
                        module_name='xml',
                        module_args=command.args,
                        task_vars=task_vars
                    )

                    self._xml_result.add(result, command)

                except Exception as e:
                    self._result.update(dict(
                        failed=True,
                        msg='Something went wrong',
                        exception=e
                    ))
                    break

        if self._is_fetch():
            self._connection = current_connection

        self._result.update(dict(
            xml=self._xml_result.operations,
            changed=self._xml_result.has_changed,
            failed=self._xml_result.has_failed,
            msg=self._xml_result.msg,
            exception=self._xml_result.exception
        ))

    def _run_module(self, module_name, task_vars, args, error_msg):
        try:
            result = self._execute_module(
                module_name=module_name,
                module_args=args.copy(),
                task_vars=task_vars
            )

            self._handle_result(result, msg=error_msg, module_name=module_name)

            return result

        except Exception as e:
            self._handle_result(
                dict(failed=True),
                msg=error_msg,
                exception=e,
                module_name=module_name
            )

    def _run_action(self, action_name, task_vars, args, error_msg):
        try:
            task = self._task.copy()
            task.args = args

            action = self._shared_loader_obj.action_loader.get(
                f'ansible.legacy.{action_name}',
                connection=self._connection,
                task=task,
                play_context=self._play_context,
                loader=self._loader,
                templar=self._templar,
                shared_loader_obj=self._shared_loader_obj
            )

            result = action.run(task_vars=task_vars)

            self._handle_result(result, msg=error_msg, module_name=action_name)

            return result

        except Exception as e:
            self._handle_result(
                dict(failed=True),
                msg=error_msg,
                exception=e,
                module_name=action_name
            )

    def _handle_result(self, result, msg=None, exception=None, module_name=None):
        if module_name:
            result.update(dict(module=module_name))

        self._result.get('sub_invocations').append(result)

        self._result.update(dict(
            changed=result.get('changed', False),
            failed=result.get('failed', False)
        ))

        if msg is not None:
            self._result.update(dict(msg=f'{msg} - {result.get("msg", "")}'))

        if exception is not None:
            self._result.update(dict(exception=exception))

    def _is_remote(self):
        return self._mode == 'remote'

    def _is_fetch(self):
        return self._mode == 'fetch'

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.base_action_module \
    import BaseActionModule
from ansible_collections.prevole.opnsense_modules.plugins.module_utils.command_builder \
    import ChangeCommandBuilder
from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command \
    import RemoveXmlCommand, CountConditionalCommand, AddEmptyXmlCommand

RECORD_FIELDS = [
    dict(name='state', skip=True),
    dict(name='descr', alias='description'),
    dict(name='host',  skip=True),
    dict(name='domain'),
    dict(name='rr', alias='record'),
    dict(name='ip'),
    dict(name='mxprio'),
    dict(name='mx')
]

ALIAS_ITEM_FIELD = [
    dict(name='state', skip=True),
    dict(name='host', skip=True),
    dict(name='domain'),
    dict(name='descr', alias='description')
]


class ActionModule(BaseActionModule):
    def __init__(self, task, connection, play_context, loader, templar, shared_loader_obj):
        super().__init__(task, connection, play_context, loader, templar, shared_loader_obj)
        self.result = None

    @property
    def module_name(self):
        return 'opnsense_unbound_record'

    def _run(self, task_vars):
        path = self._task.args.get('path')

        if self._task.args.get('state', 'present') == 'present':
            commands = self._create_or_update_commands(path)
        else:
            commands = self._remove_commands(path)

        commands = commands + self._empty_hosts_commands(path)

        self._run_commands(commands, task_vars)

    def _create_or_update_commands(self, path):
        host = self._task.args.get('host')

        command_builder = ChangeCommandBuilder(
            path=path,
            spec=RECORD_FIELDS,
            xpath_base=f'/opnsense/unbound/hosts[host/text()="{host}"]'
        )

        commands = command_builder.build(self._task.args)

        return commands + self._aliases_commands(path, host)

    def _aliases_commands(self, path, host):
        commands = []

        if 'aliases' in self._task.args:
            for alias in self._task.args['aliases']:
                xpath = f'/opnsense/unbound/hosts[host/text()="{host}"]/aliases/item[host/text()="{alias.get("host")}"]'

                if alias.get('state', 'present') == 'present':
                    alias_command_builder = ChangeCommandBuilder(
                        path=path,
                        spec=ALIAS_ITEM_FIELD,
                        xpath_base=xpath
                    )

                    commands = commands + alias_command_builder.build(alias)
                else:
                    commands = commands + [RemoveXmlCommand(
                        path=path,
                        xpath=xpath
                    )]

        return commands + self._empty_aliases_commands(path, host)


    @staticmethod
    def _empty_hosts_commands(path):
        return [
            CountConditionalCommand(
                path=path,
                xpath='/opnsense/unbound/hosts[host]',
                check=lambda count: count == 0,
                then_commands=[AddEmptyXmlCommand(
                    path=path,
                    xpath='/opnsense/unbound/hosts'
                )],
                else_commands=[RemoveXmlCommand(
                    path=path,
                    xpath='/opnsense/unbound/hosts[not(host)]'
                )]
            )
        ]

    @staticmethod
    def _empty_aliases_commands(path, host):
        return [
            CountConditionalCommand(
                path=path,
                xpath=f'/opnsense/unbound/hosts[host/text()="{host}"]/aliases/item[host]',
                check=lambda count: count == 0,
                then_commands=[AddEmptyXmlCommand(
                    path=path,
                    xpath=f'/opnsense/unbound/hosts[host/text()="{host}"]/aliases/item'
                )],
                else_commands=[RemoveXmlCommand(
                    path=path,
                    xpath=f'/opnsense/unbound/hosts[host/text()="{host}"]/aliases/item[not(host)]'
                )]
            )
        ]

    def _remove_commands(self, path):
        return [RemoveXmlCommand(
            path=path,
            xpath=f'/opnsense/unbound/hosts[host/text()="{self._task.args.get("host")}"]'
        )]

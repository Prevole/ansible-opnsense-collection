from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.base_action_module \
    import BaseActionModule
from ansible_collections.prevole.opnsense_modules.plugins.module_utils.command_builder \
    import ChangeCommandBuilder
from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command \
    import RemoveXmlCommand, CountConditionalXmlCommand, AddEmptyXmlCommand, XmlCommand


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
    @property
    def module_name(self):
        return 'opnsense_unbound_record'

    def _run(self, task_vars):
        commands: [XmlCommand] = []

        if self._task.args.get('state', 'present') == 'present':
            commands.extend(self._create_or_update_commands())
        else:
            commands.extend(self._remove_commands())

        commands.extend(empty_hosts_commands())

        self._run_commands(commands, task_vars)

    def _create_or_update_commands(self):
        host = self._task.args.get('host')

        command_builder = ChangeCommandBuilder(
            spec=RECORD_FIELDS,
            xpath_base=f'/opnsense/unbound/hosts[host/text()="{host}"]'
        )

        commands = command_builder.build(self._task.args)

        commands.extend(self._aliases_commands(host))

        return commands

    def _aliases_commands(self, host):
        commands: [XmlCommand] = []

        if 'aliases' in self._task.args:
            for alias in self._task.args['aliases']:
                xpath = f'/opnsense/unbound/hosts[host/text()="{host}"]/aliases/item[host/text()="{alias.get("host")}"]'

                if alias.get('state', 'present') == 'present':
                    alias_command_builder = ChangeCommandBuilder(
                        spec=ALIAS_ITEM_FIELD,
                        xpath_base=xpath
                    )

                    commands.extend(alias_command_builder.build(alias))
                else:
                    commands.append(RemoveXmlCommand(xpath=xpath))

        commands.extend(empty_aliases_commands(host))

        return commands

    def _remove_commands(self) -> [XmlCommand]:
        return [RemoveXmlCommand(xpath=f'/opnsense/unbound/hosts[host/text()="{self._task.args.get("host")}"]')]


def empty_aliases_commands(host) -> [XmlCommand]:
    return [
        CountConditionalXmlCommand(
            xpath=f'/opnsense/unbound/hosts[host/text()="{host}"]/aliases/item[host]',
            check=lambda count: count == 0,
            then_commands=[AddEmptyXmlCommand(xpath=f'/opnsense/unbound/hosts[host/text()="{host}"]/aliases/item')],
            else_commands=[
                RemoveXmlCommand(xpath=f'/opnsense/unbound/hosts[host/text()="{host}"]/aliases/item[not(host)]')]
        )
    ]


def empty_hosts_commands() -> [XmlCommand]:
    return [
        CountConditionalXmlCommand(
            xpath='/opnsense/unbound/hosts[host]',
            check=lambda count: count == 0,
            then_commands=[AddEmptyXmlCommand(xpath='/opnsense/unbound/hosts')],
            else_commands=[RemoveXmlCommand(xpath='/opnsense/unbound/hosts[not(host)]')]
        )
    ]

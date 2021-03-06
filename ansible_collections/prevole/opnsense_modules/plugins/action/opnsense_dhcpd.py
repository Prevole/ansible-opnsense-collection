from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.base_action_module \
    import BaseActionModule
from ansible_collections.prevole.opnsense_modules.plugins.module_utils.command_builder \
    import ChangeCommandBuilder
from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command \
    import RemoveXmlCommand

INTERFACE_FIELDS = [
    dict(name='state', skip=True),
    dict(name='enable', default=True),
    dict(name='ddnsdomainalgorithm', default='hmac-md5'),
    dict(name='tftp', empty=True),
    dict(name='netboot', empty=True),
    dict(name='nextserver', empty=True),
    dict(name='winsserver', empty=True),
    dict(name='dnsserver', empty=True),
    dict(name='ntpserver', empty=True),
    dict(name='numberoptions', values=[
        dict(name='number'),
        dict(name='type'),
        dict(name='value')
    ]),
    dict(name='range', values=[
        dict(name='from', alias='start'),
        dict(name='to', alias='end')
    ])
]

STATIC_MAP_FIELD = [
    dict(name='state', skip=True),
    dict(name='mac', skip=True),
    dict(name='ipaddr'),
    dict(name='hostname'),
    dict(name='descr', alias='description'),
    dict(name='winsserver'),
    dict(name='dnsserver'),
    dict(name='ntpserver')
]


class ActionModule(BaseActionModule):
    @property
    def module_name(self):
        return 'opnsense_dhcpd'

    def _run(self, task_vars):
        interface_name = self._task.args.get('name')

        if self._task.args.get('state', 'present') == 'present':
            commands = self._create_or_update_commands(interface_name)
        else:
            commands = _remove_commands(interface_name)

        self._run_commands(commands, task_vars)

    def _create_or_update_commands(self, interface_name):
        command_builder = ChangeCommandBuilder(
            spec=INTERFACE_FIELDS,
            xpath_base=f'/opnsense/dhcpd/{interface_name}'
        )

        commands = command_builder.build(self._task.args)

        if 'staticmap' in self._task.args:
            for static in self._task.args['staticmap']:
                if static.get('state', 'present') == 'present':
                    static_map_command_builder = ChangeCommandBuilder(
                        spec=STATIC_MAP_FIELD,
                        xpath_base=f'/opnsense/dhcpd/{interface_name}/staticmap[mac/text()="{static["mac"]}"]'
                    )

                    commands = commands + static_map_command_builder.build(static)
                else:
                    commands = commands + [RemoveXmlCommand(
                        xpath=f'/opnsense/dhcpd/{interface_name}/staticmap[mac/text()="{static["mac"]}"]')]

        return commands


def _remove_commands(interface_name):
    return [RemoveXmlCommand(xpath=f'/opnsense/dhcpd/{interface_name}')]

from ansible.plugins.action import ActionBase

INTERFACE_FIELDS = [
    'enable',
    'if',
    'ipaddr',
    'subnet',
    'ipaddrv6',
    'subnetv6',
    'track6-interface',
    'track6-prefix-id',
    'descr',
    'gateway',
    'blockpriv',
    'blockbogons',
    'dhcp6-ia-pd-len'
]

class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        result.update(self._execute_module(
            module_name='opnsense_interface',
            module_args=self._task.args,
            task_vars=task_vars
        ))

        common_args = {}

        interface_name = self._task.args.get('name')

        for elem in INTERFACE_FIELDS:
            if elem in self._task.args:
                args = common_args.copy()
                args.update({
                    'path': self._task.args.get('path'),
                    'xpath': f'/opnsense/interfaces/{interface_name}/{elem}',
                    'value': f'{self._task.args.get(elem)}',
                    'pretty_print': True
                })

                result.update(self._execute_module(
                    module_name='xml',
                    module_args=args,
                    task_vars=task_vars
                ))

        return result

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: opnsense
version_added: 2.10
short_description: OPNSense Interface module
'''


def main():
    module = AnsibleModule(
        # not checking because of daisy chain to file module
        argument_spec=dict(
            name=dict(type='str', required=True),
            path=dict(type='path', required=True),
            enable=dict(type='bool'),
            interface=dict(type='str', required=True, aliases=['if']),
            ipaddr=dict(type='str'),
            subnet=dict(type='int'),
            ipaddrv6=dict(type='str'),
            subnetv6=dict(type='int'),
            track6interface=dict(type='str', aliases=['track6-interface']),
            track6prefixid=dict(type='int', aliases=['track6-prefix-id']),
            descr=dict(type='str', required=True),
            gateway=dict(type='str', ),
            blockpriv=dict(type='str', choices=['on', 'off']),
            blockbogons=dict(type='str', choices=['on', 'off']),
            dhcp6iapdlen=dict(type='int', aliases=['dhcp6-ia-pd-len'])
        )
    )

    module.exit_json()


if __name__ == '__main__':
    main()

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: opnsense
version_added: 2.10
short_description: OPNSense DHCPd module
'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', choices=['present', 'absent'], default='present'),
            path=dict(type='path', required=True),
            name=dict(type='str', required=True),
            enable=dict(type='bool'),
            ddnsdomainalgorithm=dict(type='str', default='hmac-md5'),
            tftp=dict(type='str'),
            netboot=dict(type='str'),
            nextserver=dict(type='str'),
            winsserver=dict(type='str', aliases=['wins']),
            dnsserver=dict(type='str', aliases=['dns']),
            ntpserver=dict(type='str', aliases=['ntp']),
            numberoptions=dict(type='list', options=dict(
                number=dict(type='int', required=True),
                type=dict(type='str', required=True),
                value=dict(type='str', required=True)
            )),
            range=dict(type='dict', options=dict(
                start=dict(type='str', required=True, aliases=['from']),
                end=dict(type='str', required=True, aliases=['to'])
            )),
            staticmap=dict(type='list', options=dict(
                mac=dict(type='str', required=True, aliases=['mac_address']),
                state=dict(type='str', choices=['present', 'absent'], default='present'),
                ipaddr=dict(type='str', required=True),
                hostname=dict(type='str'),
                descr=dict(type='str'),
                winsserver=dict(type='str', aliases=['wins']),
                dnsserver=dict(type='str', aliases=['dns']),
                ntpserver=dict(type='str', aliases=['ntp'])
            ))
        )
    )

    module.exit_json()


if __name__ == '__main__':
    main()

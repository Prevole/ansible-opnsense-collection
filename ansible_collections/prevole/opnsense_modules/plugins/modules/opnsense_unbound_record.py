from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r'''
---
module: opnsense
version_added: 2.10
short_description: OPNSense Unbound Record module
'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(type='str', choices=['present', 'absent'], default='present'),
            path=dict(type='path', required=True),
            descr=dict(type='str', aliases=['description']),
            host=dict(type='str', required=True),
            domain=dict(type='str', required=True),
            record=dict(type='str', choices=['A', 'MX'], default='A'),
            ip=dict(type='str', required=True),
            mxprio=dict(type='int'),
            mx=dict(type='str'),
            aliases=dict(type='list', options=dict(
                state=dict(type='str', choices=['present', 'absent'], default='present'),
                host=dict(type='str', required=True),
                domain=dict(type='str'),
                descr=dict(type='str', aliases=['description'])
            ))
        ),
        required_if=[
            ('record', 'MX', ('mxprio', 'mx'))
        ]
    )

    module.exit_json()


if __name__ == '__main__':
    main()

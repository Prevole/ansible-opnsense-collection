from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command \
    import AddOrUpdateXmlCommand, RemoveXmlCommand
from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_result \
    import XmlResult


class TestXmlResult:
    def test_add(self):
        xml = XmlResult()

        xml.add(dict(
            changed=False,
            invocation=dict(module_args=dict(
                value='val',
                xpath='/a/b/c'
            ))
        ), AddOrUpdateXmlCommand('/a/b/c', 'val'))

        assert xml.has_changed is False
        assert xml.has_failed is False
        assert xml.operations == []

        xml.add(dict(
            changed=True,
            invocation=dict(module_args=dict(
                value='val2',
                xpath='/a/b/d'
            ))
        ), RemoveXmlCommand('/a/b/d'))

        assert xml.has_changed is True
        assert xml.has_failed is False
        assert xml.operations == [{
            'remove': '/a/b/d'
        }]

        xml.add(dict(
            changed=True,
            invocation=dict(module_args=dict(
                value='val3',
                xpath='/a/b/e'
            ))
        ), AddOrUpdateXmlCommand('/a/b/e', 'val3'))

        assert xml.has_changed is True
        assert xml.has_failed is False
        assert xml.operations == [{
            'remove': '/a/b/d'
        }, {
            'value': 'val3',
            'change': '/a/b/e'
        }]

        xml.add(dict(
            failed=True,
            msg='This is an error',
            exception=Exception(),
            invocation=dict(module_args=dict(
                value='val4',
                xpath='/a/b/f'
            ))
        ), AddOrUpdateXmlCommand('/a/b/f', 'val4'))

        assert xml.has_changed is False
        assert xml.has_failed is True
        assert xml.msg == 'This is an error'
        assert type(xml.exception) is Exception
        assert xml.operations == [{
            'remove': '/a/b/d'
        }, {
            'value': 'val3',
            'change': '/a/b/e'
        }, {
            'value': 'val4',
            'change': '/a/b/f'
        }]

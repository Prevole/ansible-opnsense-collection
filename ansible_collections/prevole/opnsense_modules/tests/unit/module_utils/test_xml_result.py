from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command import XmlCommand, \
    AddOrUpdateXmlCommand, RemoveXmlCommand
from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_result import XmlResult


class TestXmlResult:
    def test_add(self):
        xml = XmlResult()

        xml.add(dict(
            changed=False,
            invocation=dict(module_args=dict(
                value='val',
                xpath='/a/b/c'
            ))
        ), AddOrUpdateXmlCommand('config', '/a/b/c', 'val'))

        assert xml.has_changed() is False
        assert xml.operations() == []

        xml.add(dict(
            changed=True,
            invocation=dict(module_args=dict(
                value='val2',
                xpath='/a/b/d'
            ))
        ), RemoveXmlCommand('config', '/a/b/d'))

        assert xml.has_changed() is True
        assert xml.operations() == [{
            'remove': '/a/b/d'
        }]

        xml.add(dict(
            changed=True,
            invocation=dict(module_args=dict(
                value='val3',
                xpath='/a/b/e'
            ))
        ), AddOrUpdateXmlCommand('config', '/a/b/e', 'val3'))

        assert xml.has_changed() is True
        assert xml.operations() == [{
            'remove': '/a/b/d'
        }, {
            'value': 'val3',
            'change': '/a/b/e'
        }]

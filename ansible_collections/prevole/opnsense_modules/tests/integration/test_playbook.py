from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
from lxml import etree as et

from ansible_collections.prevole.opnsense_modules.tests.utils.xml_compare import xml_compare


@pytest.mark.ansible
def test_collection(ansible_playbook):
    ansible_playbook.run_playbook('collection.yml')

    for item in ['dhcpd', 'interfaces', 'unbound_records']:
        current = et.parse(f'tests/output/{item}.xml')
        expected = et.parse(f'tests/results/{item}.xml')

        assert xml_compare(current.getroot(), expected.getroot()) is True

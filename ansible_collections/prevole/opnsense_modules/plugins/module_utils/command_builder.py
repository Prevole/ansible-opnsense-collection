from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command import AddOrUpdateXmlCommand


class CommandBuilder(object):
    def __init__(self, path, spec, xpath_base):
        self.path = path
        self.spec = spec
        self.xpath_base = xpath_base
        self.commands = []


class ChangeCommandBuilder(CommandBuilder):
    def build(self, args):
        self._build(self.spec, args)
        return self.commands

    def _build(self, spec, args, xpath_base=''):
        for field_spec in spec:
            if field_spec.get('skip', False):
                continue

            field_name, module_field_name = self._detect_field_name(args, field_spec)

            if module_field_name in args:
                if 'values' in field_spec:
                    self._build(field_spec['values'], args[module_field_name], f'{xpath_base}/{field_name}')
                else:
                    self._create_command(f'{xpath_base}/{field_name}', args[module_field_name])

            elif 'default' in field_spec:
                self._create_command(f'{xpath_base}/{field_name}', field_spec['default'])

            elif field_spec.get('empty', False):
                self._create_command(f'{xpath_base}/{field_name}', None)

    def _create_command(self, xpath, value):
        self.commands.append(AddOrUpdateXmlCommand(
            path=self.path,
            xpath=f'{self.xpath_base}{xpath}',
            value=value if value is None else f'{value}'
        ))

    @staticmethod
    def _detect_field_name(args, spec):
        field_name = spec['name']

        if 'alias' in spec and spec['alias'] in args:
            module_field_name = spec['alias']
        else:
            module_field_name = field_name

        return field_name, module_field_name

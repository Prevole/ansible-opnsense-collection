from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.xml_command \
    import AddOrUpdateXmlCommand, XmlCommand


class CommandBuilder(object):
    def __init__(self, spec, xpath_base):
        self._spec = spec
        self._xpath_base = xpath_base
        self._commands: [XmlCommand] = []

    def build(self, args) -> [XmlCommand]:
        raise NotImplementedError()


class ChangeCommandBuilder(CommandBuilder):
    def build(self, args) -> [XmlCommand]:
        self._build(self._spec, args)
        return self._commands

    def _build(self, spec, args, xpath_base=''):
        for field_spec in spec:
            if field_spec.get('skip', False):
                continue

            field_name, module_field_name = detect_field_name(args, field_spec)

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
        self._commands.append(AddOrUpdateXmlCommand(
            xpath=f'{self._xpath_base}{xpath}',
            value=value if value is None else f'{value}'
        ))


def detect_field_name(args, spec):
    field_name = spec['name']

    if 'alias' in spec and spec['alias'] in args:
        module_field_name = spec['alias']
    else:
        module_field_name = field_name

    return field_name, module_field_name

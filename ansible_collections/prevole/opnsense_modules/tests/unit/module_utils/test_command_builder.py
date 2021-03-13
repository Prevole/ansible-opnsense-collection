from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.prevole.opnsense_modules.plugins.module_utils.command_builder import ChangeCommandBuilder


class TestChangeCommandBuilder:
    @staticmethod
    def _convert_result(result):
        return list(map(lambda el: el.args, result))

    def test_build_simple(self):
        spec = [
            dict(name='field1'),
            dict(name='field2')
        ]
        args = dict(
            field1='value1',
            field2='value2'
        )

        builder = ChangeCommandBuilder(spec=spec, xpath_base='/base/path')

        result = builder.build(args)

        assert self._convert_result(result) == [
            {
                'xpath': '/base/path/field1',
                'value': 'value1',
                'pretty_print': True
            },
            {
                'xpath': '/base/path/field2',
                'value': 'value2',
                'pretty_print': True
            }
        ]

    def test_build_complex(self):
        spec = [
            dict(name='field1'),
            dict(name='field2', values=[
                dict(name='sfield21', alias='subfield21'),
                dict(name='sfield22', values=[
                    dict(name='sfield221')
                ])
            ])
        ]
        args = dict(
            field1='value1',
            field2=dict(
                subfield21='svalue21',
                sfield22=dict(
                    sfield221='svalue221'
                )
            )
        )

        builder = ChangeCommandBuilder(spec=spec, xpath_base='/base/path')

        result = builder.build(args)

        assert self._convert_result(result) == [
            {
                'xpath': '/base/path/field1',
                'value': 'value1',
                'pretty_print': True
            },
            {
                'xpath': '/base/path/field2/sfield21',
                'value': 'svalue21',
                'pretty_print': True
            },
            {
                'xpath': '/base/path/field2/sfield22/sfield221',
                'value': 'svalue221',
                'pretty_print': True
            }
        ]

    def test_build_complex_with_missing_args(self):
        spec = [
            dict(name='field1'),
            dict(name='field2', values=[
                dict(name='sfield21', alias='subfield21'),
                dict(name='sfield22', values=[
                    dict(name='sfield221'),
                    dict(name='sfield222'),
                    dict(name='sfield223')
                ])
            ])
        ]
        args = dict(
            field1='value1',
            field2=dict(
                sfield22=dict(
                    sfield221='svalue221',
                    sfield223='svalue223'
                )
            )
        )

        builder = ChangeCommandBuilder(spec=spec, xpath_base='/base/path')

        result = builder.build(args)

        assert self._convert_result(result) == [
            {
                'xpath': '/base/path/field1',
                'value': 'value1',
                'pretty_print': True
            },
            {
                'xpath': '/base/path/field2/sfield22/sfield221',
                'value': 'svalue221',
                'pretty_print': True
            },
            {
                'xpath': '/base/path/field2/sfield22/sfield223',
                'value': 'svalue223',
                'pretty_print': True
            }
        ]

    def test_build_alias(self):
        spec = [
            dict(name='field1', alias='ff1'),
            dict(name='field2', alias='ff2')
        ]
        args = dict(
            field1='value1',
            ff2='value2'
        )

        builder = ChangeCommandBuilder(spec=spec, xpath_base='/base/path')

        result = builder.build(args)

        assert self._convert_result(result) == [
            {
                'xpath': '/base/path/field1',
                'value': 'value1',
                'pretty_print': True
            },
            {
                'xpath': '/base/path/field2',
                'value': 'value2',
                'pretty_print': True
            }
        ]

    def test_build_default(self):
        spec = [
            dict(name='field1', default='value1')
        ]
        args = dict()

        builder = ChangeCommandBuilder(spec=spec, xpath_base='/base/path')

        result = builder.build(args)

        assert self._convert_result(result) == [
            {
                'xpath': '/base/path/field1',
                'value': 'value1',
                'pretty_print': True
            }
        ]

    def test_build_empty(self):
        spec = [
            dict(name='field1', empty=True)
        ]
        args = dict()

        builder = ChangeCommandBuilder(spec=spec, xpath_base='/base/path')

        result = builder.build(args)

        assert self._convert_result(result) == [
            {
                'xpath': '/base/path/field1',
                'value': None,
                'pretty_print': True
            }
        ]

    def test_build_skip(self):
        spec = [
            dict(name='field0', skip=True),
            dict(name='field1', empty=True)
        ]
        args = dict()

        builder = ChangeCommandBuilder(spec=spec, xpath_base='/base/path')

        result = builder.build(args)

        assert self._convert_result(result) == [
            {
                'xpath': '/base/path/field1',
                'value': None,
                'pretty_print': True
            }
        ]

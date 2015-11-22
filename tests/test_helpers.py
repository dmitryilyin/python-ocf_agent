# -*- coding: utf-8 -*-

from ocf_agent import helpers
from unittest import TestCase
from mock import patch


class HelpersTest(TestCase):
    def test_string_to_bool(self):
        true_values = [True, 'YES', 'on', 'Y', 1, '1']
        false_values = [False, 'NO', 'off', 'N', 0, '0']
        none_values = [None, 'none', 10, 'bad value', '', 1.1, [1], {'a': 1}]
        for value in true_values:
            self.assertEquals(helpers.string_to_bool(value), True)
        for value in false_values:
            self.assertEquals(helpers.string_to_bool(value), False)
        for value in none_values:
            self.assertIsNone(helpers.string_to_bool(value))
        self.assertEquals(
            helpers.string_to_bool('bad value', True),
            True,
        )
        self.assertEquals(
            helpers.string_to_bool('bad value', False),
            False,
        )
        self.assertEquals(
            helpers.string_to_bool('bad value', 'default'),
            'default',
        )
        self.assertEquals(
            helpers.string_to_bool('YES', 'default'),
            True
        )

    def test_string_to_integer(self):
        values = {
            1: 1, 0: 0, 10: 10, -1: 1, 1.2: 1,
            '1': 1, '0': 0, '10': 10, '-10': 10,
            '2a': 2, 'a2': 2, 'a2a': 2,
            None: None, '': None, 'test': None,
        }
        for value_in, value_out in values.items():
            self.assertEquals(helpers.string_to_integer(value_in), value_out)
        self.assertEquals(
            helpers.string_to_integer('bad_value', 10),
            10,
        )
        self.assertEquals(
            helpers.string_to_integer('bad_value', 'default'),
            'default',
        )
        self.assertEquals(
            helpers.string_to_integer(1, 'default'),
            1,
        )

    def internal_function(self):
        return 'value'

    @helpers.memoization
    def memoised_function(self):
        return self.internal_function()

    def test_memoisation(self):
        with patch('tests.test_helpers.HelpersTest.internal_function') as mock:
            mock.return_value = 'value'
            self.memoised_function()
            self.memoised_function()
            self.assertEquals(mock.call_count, 1)
        self.assertEquals(self.memoised_function(), 'value')

    @helpers.docstring_format('one', 2)
    def documented_method():
        """
        A = {0}
        B = {1}
        C_
        """
        pass

    def test_docstring_format(self):
        self.assertIn('A = one', self.documented_method.__doc__)
        self.assertIn('B = 2', self.documented_method.__doc__)
        self.assertIn('C\_', self.documented_method.__doc__)

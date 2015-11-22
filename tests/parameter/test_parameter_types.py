# -*- coding: utf-8 -*-

from unittest import TestCase
from ocf_agent.parameter import BooleanParameter
from ocf_agent.parameter import IntegerParameter
from ocf_agent.parameter import StringParameter
from tests.fixtures.agents import UnitTestAgent


class OCFParameter_string_parameter(StringParameter):
    pass


class OCFParameter_integer_parameter(IntegerParameter):
    pass


class OCFParameter_boolean_parameter(BooleanParameter):
    pass


class StringParameterTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.parameters = self.agent.parameters
        self.parameter = OCFParameter_string_parameter(self.parameters)

    def tearDown(self):
        del self.parameter
        del self.parameters
        del self.agent

    def test_accepts_none_values(self):
        self.parameter.value = None
        self.assertIsNone(self.parameter.value)

    def test_accepts_str_values(self):
        self.parameter.value = 'test'
        self.assertEquals(self.parameter.value, 'test')


class IntParameterTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.parameters = self.agent.parameters
        self.parameter = OCFParameter_integer_parameter(self.parameters)

    def tearDown(self):
        del self.parameter
        del self.parameters
        del self.agent

    def test_has_type(self):
        self.assertIs(self.parameter.type, int)

    def test_has_type_name(self):
        self.assertEquals(self.parameter.type_name, 'integer')

    def test_accepts_none_values(self):
        self.parameter.value = None
        self.assertIsNone(self.parameter.value)

    def test_accepts_int_values(self):
        self.parameter.value = 1
        self.assertEquals(self.parameter.value, 1)

    def test_accepts_int_values_as_string(self):
        self.parameter.value = '2'
        self.assertEquals(self.parameter.value, 2)

    def test_does_not_accept_bad_values(self):
        self.parameter.value = 'bad value'
        self.assertIsNone(self.parameter.value)


class BoolParameterTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.parameters = self.agent.parameters
        self.parameter = OCFParameter_boolean_parameter(self.parameters)

    def tearDown(self):
        del self.parameter
        del self.parameters
        del self.agent

    def test_has_type(self):
        self.assertIs(self.parameter.type, bool)

    def test_has_type_name(self):
        self.assertEquals(self.parameter.type_name, 'boolean')

    def test_accepts_none_values(self):
        self.parameter.value = None
        self.assertIsNone(self.parameter.value)

    def test_accepts_bool_values(self):
        self.parameter.value = True
        self.assertEquals(self.parameter.value, True)
        self.parameter.value = False
        self.assertEquals(self.parameter.value, False)

    def test_accepts_bool_values_as_string(self):
        self.parameter.value = 'off'
        self.assertEquals(self.parameter.value, False)
        self.parameter.value = 'on'
        self.assertEquals(self.parameter.value, True)

    def test_does_not_accept_bad_values(self):
        self.parameter.value = 'bad value'
        self.assertIsNone(self.parameter.value)

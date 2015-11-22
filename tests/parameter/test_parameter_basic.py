# -*- coding: utf-8 -*-

from unittest import TestCase
from tests.fixtures.agents import UnitTestAgent
from ocf_agent.modules.parameters import Parameters
from ocf_agent.parameter import StringParameter
from ocf_agent.agent import Agent
from mock import patch
import os


class OCFParameter_configured_parameter(StringParameter):
    DEFAULT = 'default test value'
    LONGDESC = "Test long description"
    SHORTDESC = "Test short description"
    LANG = 'en_US'
    UNIQUE = True
    REQUIRED = True


class OCFParameter_empty_parameter(StringParameter):
    pass


class MisnamedParameter(StringParameter):
    pass


class ParameterConfiguredBasicPropertiesTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.parameters = self.agent.parameters
        self.parameter = OCFParameter_configured_parameter(self.parameters)
        os.environ = {}

    def tearDown(self):
        del self.parameter
        del self.parameters
        del self.agent

    def test_has_parameters(self):
        self.assertEquals(self.parameter.parameters, self.parameters)
        self.assertIsInstance(self.parameter.parameters, Parameters)

    def test_has_agent(self):
        self.assertEquals(self.parameter.agent, self.agent)
        self.assertIsInstance(self.parameter.agent, Agent)

    def test_has_name(self):
        self.assertEquals(self.parameter.name, 'configured_parameter')

    def test_has_short_description(self):
        self.assertEquals(self.parameter.short_description,
                          'Test short description')

    def test_has_long_description(self):
        self.assertEquals(self.parameter.long_description,
                          'Test long description')

    def test_has_language(self):
        self.assertEquals(self.parameter.language, 'en_US')

    def test_has_type(self):
        self.assertIs(self.parameter.type, str)

    def test_has_type_name(self):
        self.assertEquals(self.parameter.type_name, 'string')

    def test_has_default(self):
        self.assertEquals(self.parameter.default, 'default test value')

    def test_has_unique(self):
        self.assertEquals(self.parameter.unique, True)

    def test_has_required(self):
        self.assertEquals(self.parameter.required, True)


class ParameterEmptyBasicPropertiesTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.parameters = self.agent.parameters
        self.parameter = OCFParameter_empty_parameter(self.parameters)
        os.environ = {}

    def tearDown(self):
        del self.parameter
        del self.parameters
        del self.agent

    def test_has_name(self):
        self.assertEquals(self.parameter.name, 'empty_parameter')

    def test_has_short_description(self):
        self.assertEquals(self.parameter.short_description, 'empty_parameter')

    def test_has_long_description(self):
        self.assertEquals(self.parameter.long_description, 'empty_parameter')

    def test_has_language(self):
        self.assertEquals(self.parameter.language, 'en')

    def test_has_type(self):
        self.assertIs(self.parameter.type, str)

    def test_has_type_name(self):
        self.assertEquals(self.parameter.type_name, 'string')

    def test_has_default(self):
        self.assertEquals(self.parameter.default, None)

    def test_has_unique(self):
        self.assertEquals(self.parameter.unique, False)

    def test_has_required(self):
        self.assertEquals(self.parameter.required, False)


class ParameterLogicTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.parameters = self.agent.parameters
        self.parameter = UnitTestAgent.OCFParameter_test(self.parameters)
        os.environ = {}

    def tearDown(self):
        del self.parameter
        del self.parameters
        del self.agent

    @patch('ocf_agent.modules.exit.Exit.output')
    def test_fails_if_parameter_is_misnamed(self, mock1):
        with self.assertRaises(SystemExit):
            parameter = MisnamedParameter(self.parameters)
            parameter.validate()
        self.assertTrue(mock1.called)

    def test_knows_its_variable_name(self):
        self.assertEqual(
            self.parameter.env_variable_name,
            'OCF_RESKEY_test',
        )

    def test_uses_the_default_if_no_value(self):
        self.parameter.value = None
        self.assertEqual(self.parameter.value, self.parameter.default)
        self.assertEqual(self.parameter.value, 'test default value')

    @patch('os.environ', {'OCF_RESKEY_test': 'env value'})
    def test_can_get_value_from_environment(self):
        self.parameter.value = None
        self.assertEqual(self.parameter.value, 'env value')

    @patch('os.environ', {'OCF_RESKEY_test': 'env value'})
    def test_will_use_manually_set_value(self):
        self.parameter.value = 'manual value'
        self.assertEqual(self.parameter.value, 'manual value')

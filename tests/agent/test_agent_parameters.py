# -*- coding: utf-8 -*-
from unittest import TestCase
from ocf_agent.parameter import StringParameter
from tests.fixtures.agents import UnitTestAgent
from ocf_agent.agent import Agent
import os


class AgentParametersTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.parameters = self.agent.parameters
        os.environ = {}

    def tearDown(self):
        del self.agent
        del self.parameters

    def test_has_agent(self):
        self.assertEquals(self.parameters.agent, self.agent)
        self.assertIsInstance(self.parameters.agent, Agent)

    def test_can_get_all_parameters(self):
        self.assertIsInstance(self.parameters.all, dict)
        self.assertEquals(len(self.parameters.all.keys()), 1)

    def test_can_get_a_parameter(self):
        self.assertIsInstance(
            self.parameters.get('test'),
            StringParameter,
        )

    def test_can_get_parameter_value(self):
        self.assertEqual(self.parameters.value('test'),
                         'test default value')

    def test_can_collect_all_parameters_values(self):
        self.assertDictEqual(
            self.parameters.values, {'test': 'test default value'}
        )

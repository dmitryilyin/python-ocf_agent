# -*- coding: utf-8 -*-
from unittest import TestCase
from tests.fixtures.agents import UnitTestAgent
from ocf_agent.agent import Agent


class AgentMetaDataTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.metadata = self.agent.metadata

    def tearDown(self):
        del self.agent
        del self.metadata

    def test_has_agent(self):
        self.assertEquals(self.metadata.agent, self.agent)
        self.assertIsInstance(self.metadata.agent, Agent)

    def test_can_format_a_line(self):
        line_template = 'a: %s, b: %s, c: %d'
        line_parameters = ('test', '<test/>', 1)
        line_expected = "    a: test, b: &lt;test/&gt;, c: 1\n"
        line = self.metadata.format_line(
            2,
            line_template,
            *line_parameters
        )
        self.assertEquals(line, line_expected)

    def test_can_generate_meta_data_xml(self):
        self.maxDiff = None
        self.assertEquals(self.metadata.xml, self.agent.expected_meta_data)

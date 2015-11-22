# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch
from tests.fixtures.agents import UnitTestAgent
from tests.fixtures.agents import UnitTestEmptyAgent


class AgentConfiguredBasicPropertiesTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()

    def tearDown(self):
        del self.agent

    def test_has_name(self):
        self.assertEqual(self.agent.name, 'configured_ocf_agent')

    def test_has_short_description(self):
        self.assertEqual(self.agent.short_description,
                         'Test OCF agent')

    def test_has_long_description(self):
        self.assertEqual(self.agent.long_description, 'OCF Agent for tests')

    def test_has_language(self):
        self.assertEqual(self.agent.language, 'en_US')

    def test_has_encoding(self):
        self.assertEqual(self.agent.encoding, 'UTF-8')

    def test_has_version(self):
        self.assertEqual(self.agent.version, '0.0.1')

    @patch('sys.argv', ['test', 'monitor'])
    def test_can_get_action(self):
        self.assertEqual(self.agent.action, 'monitor')

    def test_can_set_action(self):
        self.agent.action = 'monitor'
        self.assertEqual(self.agent.action, 'monitor')

    def test_can_use_action_aliases(self):
        self.agent.action = 'status'
        self.assertEqual(self.agent.action, 'monitor')

    @patch('sys.argv', ['test'])
    @patch('ocf_agent.agent.Agent.usage')
    @patch('ocf_agent.modules.exit.Exit.output')
    def test_fails_if_no_action_set(self, mock1, mock2):
        with self.assertRaises(SystemExit):
            self.agent.validate()
        self.assertTrue(mock1.called)
        self.assertTrue(mock2.called)

    @patch('sys.argv', ['test', 'test'])
    @patch('ocf_agent.agent.Agent.usage')
    @patch('ocf_agent.modules.exit.Exit.output')
    def test_fails_if_bad_action(self, mock1, mock2):
        with self.assertRaises(SystemExit):
            self.agent.validate()
        self.assertTrue(mock1.called)
        self.assertTrue(mock2.called)


class AgentEmptyBasicPropertiesTest(TestCase):
    def setUp(self):
        self.agent = UnitTestEmptyAgent()

    def tearDown(self):
        del self.agent

    def test_has_name(self):
        self.assertEqual(self.agent.name, 'UnitTestEmptyAgent')

    def test_has_short_description(self):
        self.assertEqual(self.agent.short_description, 'UnitTestEmptyAgent')

    def test_has_long_description(self):
        self.assertEqual(self.agent.long_description, 'UnitTestEmptyAgent')

    def test_has_language(self):
        self.assertEqual(self.agent.language, 'en')

    def test_has_encoding(self):
        self.assertEqual(self.agent.encoding, 'utf-8')

    def test_has_version(self):
        self.assertEqual(self.agent.version, '1')

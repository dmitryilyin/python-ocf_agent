# -*- coding: utf-8 -*-
from unittest import TestCase
from mock import patch
from mock import PropertyMock
from tests.fixtures.agents import UnitTestAgent
from ocf_agent.handler import MonitorHandler
from ocf_agent.handler import Handler
from ocf_agent.agent import Agent


class AgentHandlersTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.handlers = self.agent.handlers

    def tearDown(self):
        del self.agent
        del self.handlers

    def test_has_agent(self):
        self.assertEquals(self.handlers.agent, self.agent)
        self.assertIsInstance(self.handlers.agent, Agent)

    def test_can_get_all_handlers(self):
        handlers = self.handlers.all
        self.assertIsInstance(handlers, list)
        self.assertEquals(len(handlers), 4)

    def test_can_get_a_handler(self):
        action = 'start'
        handler = self.handlers.get(action=action)
        self.assertIsInstance(handler, Handler)
        self.assertEquals(handler.action, action)

    def test_can_get_the_monitor_handler_with_a_specific_depth(self):
        action = 'monitor'
        got_handler = self.handlers.get(action=action, check_level=10)
        self.assertIsInstance(got_handler, MonitorHandler)
        self.assertEquals(got_handler.depth, 10)
        got_handler = self.handlers.get(action=action, check_level=0)
        self.assertIsInstance(got_handler, MonitorHandler)
        self.assertEquals(got_handler.depth, 0)

    def test_can_get_any_monitor_action_as_a_fallback(self):
        action = 'monitor'
        depth = 100
        got_handler = self.handlers.get(action=action, check_level=depth)
        self.assertIsInstance(got_handler, MonitorHandler)
        self.assertIn(got_handler.depth, [0, 10])

    def test_can_get_all_defined_handler_action(self):
        defined_actions = self.handlers.actions
        expected_actions = self.agent.expected_defined_handler_actions
        self.assertEquals(defined_actions, expected_actions)
        self.assertIsInstance(defined_actions, set)

    def test_can_get_the_current_handler(self):
        self.agent.action = 'start'
        self.assertIsInstance(
            self.handlers.current,
            Handler,
        )
        self.assertEquals(
            self.handlers.current.action,
            self.agent.action,
        )

    def test_can_get_the_correct_current_monitor_handler(self):
        with patch('ocf_agent.modules.environment.Environment.check_level',
                   new_callable=PropertyMock) as check_level_mock:
            check_level_mock.return_value = 10
            self.agent.action = 'monitor'
            self.assertIsInstance(
                self.handlers.current,
                MonitorHandler,
            )
            self.assertEquals(
                self.handlers.current.action,
                self.agent.action,
            )
            self.assertEquals(self.handlers.current.depth, 10)
            check_level_mock.return_value = 0
            self.assertEquals(self.handlers.current.depth, 0)

    def test_can_get_the_current_handler_attributes(self):
        self.agent.action = 'monitor'
        attributes = self.handlers.current.attributes
        self.assertIsInstance(attributes, dict)
        self.assertEquals(attributes, self.agent.expected_monitor_attributes)

    def test_can_get_all_handlers_attributes(self):
        attributes = self.handlers.attributes
        self.assertIsInstance(attributes, dict)
        self.assertDictEqual(
            attributes,
            self.agent.expected_handlers_attributes,
        )

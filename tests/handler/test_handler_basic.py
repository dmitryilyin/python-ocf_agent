# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch
from tests.fixtures.agents import UnitTestAgent
from ocf_agent.modules.handlers import Handlers
from ocf_agent.handler import Handler
from ocf_agent.agent import Agent


class MisnamedHandler(Handler):
    pass


class HandlerStartPropertyTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.handlers = self.agent.handlers
        self.handler = UnitTestAgent.OCFHandler_start(self.handlers)

    def tearDown(self):
        del self.handler
        del self.agent
        del self.handlers

    def test_has_handlers(self):
        self.assertEquals(self.handler.handlers, self.handlers)
        self.assertIsInstance(self.handler.handlers, Handlers)

    def test_has_agent(self):
        self.assertEquals(self.handler.agent, self.agent)
        self.assertIsInstance(self.handler.agent, Agent)

    def test_has_name(self):
        self.assertEquals(self.handler.name, 'start')
        self.assertEquals(self.handler.action, 'start')

    @patch('ocf_agent.modules.exit.Exit.output')
    def test_fails_if_handler_is_misnamed(self, mock1):
        with self.assertRaises(SystemExit):
            handler = MisnamedHandler(self.handlers)
            handler.validate()
        self.assertTrue(mock1.called)

    def test_has_short_description(self):
        self.assertEquals(self.handler.short_description,
                          'start')

    def test_has_long_description(self):
        self.assertEquals(self.handler.long_description,
                          'start')

    def test_has_language(self):
        self.assertEquals(self.handler.language, 'en')

    def test_has_timeout(self):
        self.assertEquals(self.handler.timeout, 20)

    def test_has_default_method_name(self):
        self.assertEqual(self.handler.default_method_name, 'handler_start')

    def test_has_method_name(self):
        self.assertEquals(self.handler.method_name, 'handler_start')

    def test_has_method(self):
        self.assertEquals(self.agent.handler_start, self.handler.method)

    @patch('tests.fixtures.agents.UnitTestAgent.handler_start')
    def test_can_call_the_method(self, mock1):
        self.handler.call()
        self.assertTrue(mock1.called)


class HandlerStopPropertyTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.handlers = self.agent.handlers
        self.handler = UnitTestAgent.OCFHandler_StopHandler(self.handlers)

    def tearDown(self):
        del self.handler
        del self.agent
        del self.handlers

    def test_has_name(self):
        self.assertEquals(self.handler.name, 'stop')
        self.assertEquals(self.handler.action, 'stop')
        self.assertEquals(self.handler.full_name, 'stop')

    def test_has_short_description(self):
        self.assertEquals(self.handler.short_description,
                          'Stop handler')

    def test_has_long_description(self):
        self.assertEquals(self.handler.long_description,
                          'The configured stop handler')

    def test_has_language(self):
        self.assertEquals(self.handler.language, 'en_US')

    def test_has_timeout(self):
        self.assertEquals(self.handler.timeout, 30)

    def test_has_default_method_name(self):
        self.assertEqual(self.handler.default_method_name, 'handler_stop')

    def test_has_method_name(self):
        self.assertEquals(self.handler.method_name, 'stop_agent')

    def test_has_method(self):
        self.assertEquals(self.agent.stop_agent, self.handler.method)

    @patch('tests.fixtures.agents.UnitTestAgent.stop_agent')
    def test_can_call_the_method(self, mock1):
        self.handler.call()
        self.assertTrue(mock1.called)

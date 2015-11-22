# -*- coding: utf-8 -*-

from unittest import TestCase
from tests.fixtures.agents import UnitTestAgent


class HandlerMonitorBasicTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.handlers = self.agent.handlers
        self.handler = UnitTestAgent.OCFHandler_monitor(self.handlers)

    def tearDown(self):
        del self.handler
        del self.agent
        del self.handlers

    def test_has_full_name(self):
        self.assertEquals(self.handler.name, 'monitor')
        self.assertEquals(self.handler.action, 'monitor')
        self.assertEquals(self.handler.full_name, 'monitor')

    def test_has_monitor_method_name(self):
        self.assertEquals(
            self.handler.method_name,
            'handler_monitor',
        )

    def test_can_get_monitor_method(self):
        self.assertEquals(
            self.handler.method,
            self.agent.handler_monitor,
        )

    def test_has_interval(self):
        self.assertEquals(self.handler.interval, 10)

    def test_has_depth(self):
        self.assertEquals(self.handler.depth, 0)

    def test_has_role(self):
        self.assertEquals(self.handler.role, None)


class HandlerMonitorConfiguredTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.handlers = self.agent.handlers
        self.handler = UnitTestAgent.OCFHandler_monitor_long(self.handlers)

    def tearDown(self):
        del self.handler
        del self.agent
        del self.handlers

    def test_has_full_name(self):
        self.assertEquals(self.handler.name, 'monitor')
        self.assertEquals(self.handler.action, 'monitor')
        self.assertEquals(self.handler.full_name, 'monitor_master_10')

    def test_has_monitor_method_name(self):
        self.assertEquals(
            self.handler.method_name,
            'handler_monitor_long',
        )

    def test_can_get_monitor_method(self):
        self.assertEquals(
            self.handler.method,
            self.agent.handler_monitor_long,
        )

    def test_has_interval(self):
        self.assertEquals(self.handler.interval, 60)

    def test_has_depth(self):
        self.assertEquals(self.handler.depth, 10)

    def test_has_role(self):
        self.assertEquals(self.handler.role, 'Master')

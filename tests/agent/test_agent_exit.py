# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch
from ocf_agent.agent import Agent
from tests.fixtures.agents import UnitTestAgent


class TestAgentExit(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.exit = self.agent.exit

    def tearDown(self):
        del self.agent
        del self.exit

    def test_has_agent(self):
        self.assertEquals(self.exit.agent, self.agent)
        self.assertIsInstance(self.exit.agent, Agent)

    @patch('ocf_agent.modules.log.Log.info')
    def test_can_send_a_string_to_the_log(self, mock1):
        self.exit.output('test event', 'test message', 0)
        mock1.assert_called_once_with(
            'test event: test message - exit code: 0'
        )


exit_events = {
    'success': 0,
    'error_generic': 1,
    'error_arguments': 2,
    'error_unimplemented': 3,
    'error_permissions': 4,
    'error_installation': 5,
    'error_configuration': 6,
    'not_running': 7,
    'running_master': 8,
    'master_failed': 9,
}

for event, return_code in exit_events.items():
    @patch('ocf_agent.modules.exit.Exit.output')
    def function_test(self, mock1):
        message = '%s message' % event
        with self.assertRaises(SystemExit) as context:
            method = getattr(self.exit, event)
            method(message)
        mock1.assert_called_once_with(
            event,
            message,
            return_code,
        )
        self.assertEquals(context.exception.code, return_code)

    function_name = 'test_can_exit_with_%s' % event
    function_test.__name__ = function_name
    setattr(TestAgentExit, function_name, function_test)

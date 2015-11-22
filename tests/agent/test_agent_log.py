# -*- coding: utf-8 -*-

import logging
import logging.handlers
import sys
from unittest import TestCase
from tests.fixtures.agents import UnitTestAgent
from tests.fixtures.agents import UnitTestEmptyAgent
from ocf_agent.agent import Agent
from mock import patch


class TestLogAgent(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.log = self.agent.log

    def tearDown(self):
        del self.agent
        del self.log

    def test_has_agent(self):
        self.assertEquals(self.log.agent, self.agent)
        self.assertIsInstance(self.log.agent, Agent)

    def test_can_return_the_logger_object(self):
        self.assertIsInstance(self.log.logger, logging.Logger)

    def logger_object_hash_configured_handlers(self):
        with patch('ocf_agent.modules.log.Log.enabled_handlers') as mock1:
            mock1.return_value = ['console']
            self.assertEqual(
                self.log.logger.handlers,
                [self.log.handler_console],
            )
            mock1.return_value = ['file']
            self.assertEqual(
                self.log.logger.handlers,
                [self.log.handler_file],
            )
            mock1.return_value = ['syslog']
            self.assertEqual(
                self.log.logger.handlers,
                [self.log.handler_syslog],
            )

    def test_can_get_console_handler(self):
        self.assertIsInstance(self.log.handler_console, logging.StreamHandler)
        self.assertEqual(self.log.handler_console.stream, sys.stderr)

    def test_can_get_file_handler(self):
        self.assertIsInstance(self.log.handler_file, logging.FileHandler)
        self.assertEqual(
            self.log.handler_file.baseFilename,
            self.log.log_file_path
        )

    def test_can_get_all_formatters(self):
        self.assertIsInstance(self.log.formatter_file, logging.Formatter)
        self.assertIsInstance(self.log.formatter_console, logging.Formatter)
        self.assertIsInstance(self.log.formatter_syslog, logging.Formatter)

    @patch('ocf_agent.modules.environment.Environment.log_facility', 'test')
    def test_can_get_syslog_handler(self):
        self.assertIsInstance(
            self.log.handler_syslog,
            logging.handlers.SysLogHandler,
        )
        self.assertEqual(
            self.log.handler_syslog.facility,
            'test',
        )

    def test_has_format_properties(self):
        self.assertTrue(hasattr(self.log, 'format_date'))
        self.assertTrue(hasattr(self.log, 'format_date_prefix'))
        self.assertTrue(hasattr(self.log, 'format_suffix'))

    def test_can_get_enabled_handlers(self):
        self.assertEqual(self.log.enabled_handlers, ['console'])

    def test_can_get_default_enabled_handlers(self):
        empty_agent = UnitTestEmptyAgent()
        self.assertEqual(
            empty_agent.log.enabled_handlers, ['console', 'syslog']
        )
        del empty_agent

    @patch('ocf_agent.modules.environment.Environment.is_debug', False)
    def test_can_get_normal_log_level(self):
        self.assertEqual(self.log.level, logging.INFO)

    @patch('ocf_agent.modules.environment.Environment.is_debug', True)
    def test_can_get_debug_log_level(self):
        self.assertEqual(self.log.level, logging.DEBUG)

    @patch('sys.stdout')
    def test_can_write_to_output(self, mock1):
        mock1.write.return_value = None
        self.log.output('test')
        mock1.write.assert_called_once_with('test')

    def test_has_log_methods(self):
        methods = [
            'log', 'debug', 'info', 'warning', 'warn', 'error', 'err',
            'critical', 'crit', 'exception',
        ]
        for method in methods:
            self.assertTrue(hasattr(self.log, method))

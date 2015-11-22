# -*- coding: utf-8 -*-
from unittest import TestCase
from tests.fixtures.agents import UnitTestAgent
from ocf_agent.agent import Agent
from mock import patch


class TestPidAgent(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.pid = self.agent.pid

    def tearDown(self):
        del self.agent
        del self.pid

    def test_has_agent(self):
        self.assertEquals(self.pid.agent, self.agent)
        self.assertIsInstance(self.pid.agent, Agent)

    def test_hash_directory(self):
        self.assertEqual(self.pid.directory, '/var/run/pacemaker')

    @patch(
        'ocf_agent.modules.environment.Environment.res_instance',
        'unit_test_agent')
    def test_can_make_file_name(self):
        self.assertEqual(
            self.pid.file_name(),
            'configured_ocf_agent-unit_test_agent.pid',
        )
        self.assertEqual(
            self.pid.file_name('test'),
            'configured_ocf_agent-unit_test_agent-test.pid',
        )

    @patch(
        'ocf_agent.modules.environment.Environment.res_instance',
        'unit_test_agent')
    def test_can_make_file_path(self):
        self.assertEqual(
            self.pid.file_path(),
            '/var/run/pacemaker/'
            'configured_ocf_agent-unit_test_agent.pid',
        )
        self.assertEqual(
            self.pid.file_path('test'),
            '/var/run/pacemaker/'
            'configured_ocf_agent-unit_test_agent-test.pid',
        )

    @patch('os.mkdir')
    @patch('os.path')
    def test_can_make_directory(self, mock1, mock2):
        mock2.return_value = None
        mock1.isdir.return_value = False
        self.pid.make_directory()
        mock2.assert_called_once_with('/var/run/pacemaker')
        mock2.reset_mock()
        mock1.isdir.return_value = True
        self.pid.make_directory()
        self.assertFalse(mock2.called)

    @patch('ocf_agent.modules.pid.Pid.file_path',
           return_value='/path/to/file')
    @patch('os.path')
    def test_can_check_that_file_is_present(self, mock1, mock2):
        mock1.isfile.return_value = True
        self.assertTrue(self.pid.is_present)
        mock1.isfile.assert_called_once_with('/path/to/file')
        mock1.isfile.return_value = False
        self.assertFalse(self.pid.is_present)
        self.assertTrue(mock2.called)

    # @patch('ocf_agent.modules.pid.Pid.file_path',
    #        return_value='/path/to/file')
    # @patch('ocf_agent.modules.pid.Pid.make_directory', return_value=None)
    # def test_can_create_file(self, mock1, mock2):
    #     with patch('ocf_agent.modules.pid.Pid.open', mock_open()) as mock3:
    #         self.pid.create_file(1)
    #     self.assertTrue(mock1.called)
    #     self.assertTrue(mock2.called)
    #     mock3.assert_called_once_with('/path/to/file', 'w')
    #     mock3().write.assert_called_once_with("1\n")

    @patch('os.remove')
    @patch('ocf_agent.modules.pid.Pid.file_path',
           return_value='/path/to/file')
    @patch(
        'ocf_agent.modules.pid.Pid.file_is_present',
        return_value=True)
    def test_can_remove_file(self, mock1, mock2, mock3):
        self.pid.remove_file()
        self.assertTrue(mock1.called)
        self.assertTrue(mock2.called)
        self.assertTrue(mock3.called)
        mock3.assert_called_once_with('/path/to/file')

    # @patch('ocf_agent.modules.pid.Pid.file_path',
    #        return_value='/path/to/file')
    # @patch(
    #     'ocf_agent.modules.pid.Pid.file_is_present',
    #     return_value=True)
    # def test_can_read_file(self, mock1, mock2):
    #     open_name = '%s.open' % __name__
    #     with patch(open_name, mock_open(read_data="1\n")) as mock3:
    #         pid = self.pid.read_file()
    #     self.assertTrue(mock1.called)
    #     self.assertTrue(mock2.called)
    #     mock3.assert_called_once_with('/path/to/file', 'r')
    #     self.assertEqual(pid, 1)

# -*- coding: utf-8 -*-
from unittest import TestCase
from tests.fixtures.agents import UnitTestAgent
from ocf_agent.agent import Agent
from mock import patch


class TestLockAgent(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.lock = self.agent.lock

    def tearDown(self):
        del self.agent
        del self.lock

    def test_has_agent(self):
        self.assertEquals(self.lock.agent, self.agent)
        self.assertIsInstance(self.lock.agent, Agent)

    def test_hash_directory(self):
        self.assertEqual(self.lock.directory, '/var/lock/pacemaker')

    @patch(
        'ocf_agent.modules.environment.Environment.res_instance',
        'unit_test_agent')
    def test_can_make_file_name(self):
        self.assertEqual(
            self.lock.file_name(),
            'configured_ocf_agent-unit_test_agent.lock',
        )
        self.assertEqual(
            self.lock.file_name('test'),
            'configured_ocf_agent-unit_test_agent-test.lock',
        )

    @patch(
        'ocf_agent.modules.environment.Environment.res_instance',
        'unit_test_agent')
    def test_can_make_file_path(self):
        self.assertEqual(
            self.lock.file_path(),
            '/var/lock/pacemaker/'
            'configured_ocf_agent-unit_test_agent.lock',
        )
        self.assertEqual(
            self.lock.file_path('test'),
            '/var/lock/pacemaker/'
            'configured_ocf_agent-unit_test_agent-test.lock',
        )

    @patch('os.mkdir')
    @patch('os.path')
    def test_can_make_directory(self, mock1, mock2):
        mock2.return_value = None
        mock1.isdir.return_value = False
        self.lock.make_directory()
        mock2.assert_called_once_with('/var/lock/pacemaker')
        mock2.reset_mock()
        mock1.isdir.return_value = True
        self.lock.make_directory()
        self.assertFalse(mock2.called)

    @patch('ocf_agent.modules.lock.Lock.file_path',
           return_value='/path/to/file')
    @patch('os.path')
    def test_can_check_that_file_is_present(self, mock1, mock2):
        mock1.isfile.return_value = True
        self.assertTrue(self.lock.file_is_present())
        mock1.isfile.assert_called_once_with('/path/to/file')
        mock1.isfile.return_value = False
        self.assertFalse(self.lock.file_is_present())
        self.assertTrue(mock2.called)

    # @patch('ocf_agent.modules.lock.Lock.file_path',
    #        return_value='/path/to/file')
    # @patch('ocf_agent.modules.lock.Lock.make_directory', return_value=None)
    # def test_can_create_file(self, mock1, mock2):
    #     with patch('ocf_agent.modules.lock.Lock.open', mock_open()) as mock3:
    #         self.lock.create_file()
    #     self.assertTrue(mock1.called)
    #     self.assertTrue(mock2.called)
    #     mock3.assert_called_once_with('/path/to/file', 'w')
    #     self.assertTrue(mock3().close.called)

    @patch('os.remove')
    @patch('ocf_agent.modules.lock.Lock.file_path',
           return_value='/path/to/file')
    @patch(
        'ocf_agent.modules.lock.Lock.file_is_present',
        return_value=True)
    def test_can_remove_file(self, mock1, mock2, mock3):
        self.lock.remove_file()
        self.assertTrue(mock1.called)
        self.assertTrue(mock2.called)
        self.assertTrue(mock3.called)
        mock3.assert_called_once_with('/path/to/file')

# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import patch
from tests.fixtures.agents import UnitTestAgent
from ocf_agent.agent import Agent
import os


class AgentEnvTest(TestCase):
    def setUp(self):
        self.agent = UnitTestAgent()
        self.environment = self.agent.environment
        os.environ = {}

    def tearDown(self):
        del self.agent
        del self.environment

    def test_has_agent(self):
        self.assertEquals(self.environment.agent, self.agent)
        self.assertIsInstance(self.environment.agent, Agent)

    @patch('os.environ', {'OCF_RESOURCE_TYPE': 'test_type'})
    def test_can_get_resource_type(self):
        self.assertEqual(self.environment.res_type, 'test_type')

    def test_default_resource_type(self):
        self.assertEqual(self.environment.res_type, None)

    @patch('os.environ', {'OCF_RESOURCE_PROVIDER': 'test_provider'})
    def test_can_get_resource_provider(self):
        self.assertEqual(self.environment.res_provider, 'test_provider')

    def test_default_resource_provider(self):
        self.assertEqual(self.environment.res_provider, None)

    def test_can_get_resource_class(self):
        self.assertEqual(self.environment.res_class, 'ocf')

    @patch('os.environ', {'OCF_RESOURCE_INSTANCE': 'test_instance'})
    def test_can_get_resource_instance(self):
        self.assertEqual(self.environment.res_instance, 'test_instance')
        self.assertEqual(self.environment.instance_name, 'test_instance')
        self.assertEqual(self.environment.instance, 'test_instance')
        self.assertEqual(self.environment.instance_suffix, None)

    @patch('os.environ', {'OCF_RESOURCE_INSTANCE': 'test_instance:1'})
    def test_can_get_resource_instance_with_number(self):
        self.assertEqual(self.environment.res_instance, 'test_instance:1')
        self.assertEqual(self.environment.instance_name, 'test_instance')
        self.assertEqual(self.environment.instance, 'test_instance')
        self.assertEqual(self.environment.instance_suffix, '1')

    def test_default_resource_instance(self):
        self.assertEqual(self.environment.res_instance, self.agent.name)
        self.assertEqual(self.environment.instance_name, self.agent.name)
        self.assertEqual(self.environment.instance, self.agent.name)
        self.assertEqual(self.environment.instance_suffix, None)

    @patch('os.environ', {'OCF_CHECK_LEVEL': '20'})
    def test_can_get_resource_check_level(self):
        self.assertEqual(self.environment.check_level, 20)
        self.assertEqual(self.environment.depth, self.environment.check_level)

    def test_default_check_level(self):
        self.assertEqual(self.environment.check_level, 0)
        self.assertEqual(self.environment.depth, 0)

    @patch('os.environ', {'OCF_RA_VERSION_MAJOR': '2'})
    def test_can_get_ra_version_major(self):
        self.assertEqual(self.environment.ra_version_major, 2)

    def test_can_get_default_ra_version_major(self):
        self.assertEqual(self.environment.ra_version_major, 1)

    @patch('os.environ', {'OCF_RA_VERSION_MINOR': '1'})
    def test_can_get_ra_version_minor(self):
        self.assertEqual(self.environment.ra_version_minor, 1)

    def test_can_get_default_ra_version_minor(self):
        self.assertEqual(self.environment.ra_version_minor, 0)

    @patch('os.environ', {'HA_debug': '1'})
    def test_can_get_ha_debug(self):
        self.assertEqual(self.environment.is_debug, True)

    @patch('os.environ', {'HA_debug': 'bad_value'})
    def test_can_get_invalid_ha_debug(self):
        self.assertEquals(self.environment.is_debug, False)

    def test_can_get_default_ha_debug(self):
        self.assertEqual(self.environment.is_debug, False)

    @patch('os.environ', {'HA_LOGD': 'yes'})
    def test_can_get_ha_logd(self):
        self.assertEqual(self.environment.is_logd, True)

    @patch('os.environ', {'HA_LOGD': 'bad_value'})
    def test_can_get_invalid_ha_logd(self):
        self.assertEqual(self.environment.is_logd, False)

    def test_can_get_default_ha_logd(self):
        self.assertEqual(self.environment.is_logd, False)

    @patch('os.environ', {'HA_LOGFACILITY': 'user'})
    def test_can_get_ha_log_facility(self):
        self.assertEqual(self.environment.log_facility, 'user')

    def test_can_get_default_ha_log_facility(self):
        self.assertEqual(self.environment.log_facility, 'daemon')

    @patch('os.environ', {'OCF_ROOT': '/usr/local/lib/ocf'})
    def test_can_get_ocf_root(self):
        self.assertEqual(self.environment.ocf_root, '/usr/local/lib/ocf')

    def test_can_get_default_ocf_root(self):
        self.assertEqual(self.environment.ocf_root, '/usr/lib/ocf')

    @patch('os.environ', {'HA_cluster_type': 'heartbeat'})
    def test_can_get_cluster_type(self):
        self.assertEqual(self.environment.cluster_type, 'heartbeat')

    def test_can_get_default_cluster_type(self):
        self.assertEqual(self.environment.cluster_type, 'corosync')

    @patch('os.environ', {'HA_quorum_type': 'heartbeat'})
    def test_can_get_quorum_type(self):
        self.assertEqual(self.environment.quorum_type, 'heartbeat')

    def test_can_get_default_quorum_type(self):
        self.assertEqual(self.environment.quorum_type, 'pcmk')

    @patch('os.environ', {'OCF_RESKEY_CRM_meta_master_max': '1'})
    def test_can_get_meta_master_max(self):
        self.assertEqual(self.environment.meta_master_max, 1)
        self.assertEqual(self.environment.is_ms, True)

    def test_can_get_default_meta_master_max(self):
        self.assertEqual(self.environment.meta_master_max, None)
        self.assertEqual(self.environment.is_ms, False)

    @patch('os.environ', {'OCF_RESKEY_CRM_meta_clone_max': '1'})
    def test_can_get_meta_clone_max(self):
        self.assertEqual(self.environment.meta_clone_max, 1)
        self.assertEqual(self.environment.is_clone, True)

    def test_can_get_default_meta_clone_max(self):
        self.assertEqual(self.environment.meta_clone_max, None)
        self.assertEqual(self.environment.is_clone, False)

    @patch('os.environ', {'OCF_RESKEY_CRM_meta_master': '1'})
    def test_can_get_meta_master(self):
        self.assertEqual(self.environment.meta_master, 1)

    def test_can_get_default_meta_master(self):
        self.assertEqual(self.environment.meta_master, None)

    @patch('os.environ', {'OCF_RESKEY_CRM_meta_clone': '1'})
    def test_can_get_meta_clone(self):
        self.assertEqual(self.environment.meta_clone, 1)

    def test_can_get_default_meta_clone(self):
        self.assertEqual(self.environment.meta_clone, None)

    @patch('os.environ', {
        'OCF_a': '1',
        'HA_b': '2',
        'C': '3'})
    def test_can_collect_environment(self):
        self.assertDictEqual(self.environment.all,
                             {'HA_b': '2', 'OCF_a': '1'})

    def test_default_environment(self):
        self.assertDictEqual(self.environment.all, {})

    @patch('os.environ', {
        'OCF_RESKEY_CRM_meta_a': '1',
        'OCF_RESKEY_CRM_meta_b': '2',
        'C': '3'})
    def test_can_collect_meta_environment(self):
        self.assertDictEqual(self.environment.meta,
                             {'b': '2', 'a': '1'})

    def test_default_meta_environment(self):
        self.assertDictEqual(self.environment.meta, {})

    @patch('os.environ', {
        'OCF_RESKEY_CRM_meta_notify_a': '1',
        'OCF_RESKEY_CRM_meta_notify_b': '2',
        'C': '3'})
    def test_can_collect_notify_environment(self):
        self.assertDictEqual(self.environment.notify,
                             {'b': '2', 'a': '1'})

    def test_default_notify_environment(self):
        self.assertDictEqual(self.environment.notify, {})

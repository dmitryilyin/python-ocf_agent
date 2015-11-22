# -*- coding: utf-8 -*-
# flake8: noqa
from ocf_agent.agent import Agent
from ocf_agent.parameter import StringParameter
from ocf_agent.handler import MonitorHandler
from ocf_agent.handler import Handler


class UnitTestAgent(Agent):
    VERSION = "0.0.1"
    SHORTDESC = "Test OCF agent"
    LONGDESC = "OCF Agent for tests"
    LANG = 'en_US'
    ENCODING = 'UTF-8'
    NAME = 'configured_ocf_agent'
    LOG_HANDLERS = ['console']

    class OCFParameter_test(StringParameter):
        DEFAULT = 'test default value'
        LONGDESC = "Test parameter description"
        SHORTDESC = "Test parameter"

    class OCFHandler_start(Handler):
        pass

    class OCFHandler_StopHandler(Handler):
        ACTION = 'stop'
        LONGDESC = "The configured stop handler"
        SHORTDESC = "Stop handler"
        LANG = 'en_US'
        TIMEOUT = '30'
        METHOD = 'stop_agent'

    class OCFHandler_monitor(MonitorHandler):
        pass

    class OCFHandler_monitor_long(MonitorHandler):
        DEPTH = '10'
        INTERVAL = '60'
        ROLE = 'master'
        METHOD = 'handler_monitor_long'

    ##########

    def handler_start(self):
        pass

    def stop_agent(self):
        pass

    def handler_monitor(self):
        pass

    def handler_monitor_long(self):
        pass

    @property
    def expected_handlers_attributes(self):
        return {
            'monitor': {
                'name': 'monitor',
                'timeout': 20,
                'depth': 0,
                'interval': 10,
            },
            'monitor_master_10': {
                'name': 'monitor',
                'timeout': 20,
                'depth': 10,
                'interval': 60,
                'role': 'Master',
            },
            'stop': {
                'name': 'stop',
                'timeout': 30,
            },
            'start': {
                'name': 'start',
                'timeout': 20.
            },
        }

    @property
    def expected_meta_data(self):
        return '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE resource-agent SYSTEM "ra-api-1.dtd">
<resource-agent name="configured_ocf_agent" version="0.0.1">
  <version>0.0.1</version>
  <longdesc lang="en_US">OCF Agent for tests</longdesc>
  <shortdesc lang="en_US">Test OCF agent</shortdesc>
  <parameters>
    <parameter name="test" unique="0" required="0">
      <longdesc lang="en">Test parameter description</longdesc>
      <shortdesc lang="en">Test parameter</shortdesc>
      <content type="string" default="test default value"/>
    </parameter>
  </parameters>
  <actions>
    <action name="stop" timeout="30"/>
    <action name="monitor" timeout="20" interval="10" depth="0"/>
    <action name="monitor" timeout="20" interval="60" depth="10" role="Master"/>
    <action name="start" timeout="20"/>
  </actions>
</resource-agent>
'''

    @property
    def expected_start_attributes(self):
        return self.expected_handlers_attributes['start']

    @property
    def expected_monitor_attributes(self):
        return self.expected_handlers_attributes['monitor']

    @property
    def expected_monitor_long_attributes(self):
        return self.expected_handlers_attributes['monitor_10']

    @property
    def expected_defined_handler_actions(self):
        return {
            'status', 'monitor', 'meta-data',
            'validate-all', 'usage', 'help',
            'restart', 'validate', 'meta',
            'start', 'stop'
        }


class UnitTestEmptyAgent(Agent):
    pass

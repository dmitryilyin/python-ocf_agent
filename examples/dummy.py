#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ocf_agent.agent import Agent
from ocf_agent.parameter import StringParameter
from ocf_agent.handler import Handler
from ocf_agent.handler import MonitorHandler


class DummyOCF(Agent):
    VERSION = "1.0"
    LOCK_DIR = '/tmp'
    SHORTDESC = "Dummy OCF agent"
    LONGDESC = "This OCF agent does nothing. It can be used for testing in" \
               "both simple and master modes."
    LOG_HANDLERS = ['console']

    # PARAMETERS #

    class OCFParameter_fake(StringParameter):
        DEFAULT = 'fake value'
        LONGDESC = "A fake parameter that has no effect"
        SHORTDESC = "A fake parameter"

    # HANDLERS #

    class OCFHandler_start(Handler):
        LONGDESC = "Start the dummy service"
        SHORTDESC = "Start service"

    class OCFHandler_stop(Handler):
        LONGDESC = "Stop the dummy service"
        SHORTDESC = "Stop service"

    class OCFHandler_reload(Handler):
        LONGDESC = "Reload the dummy service"
        SHORTDESC = "Reload service"

    class OCFHandler_monitor(MonitorHandler):
        LONGDESC = "Monitor the dummy service"
        SHORTDESC = "Monitor service"

    class OCFHandler_promote(Handler):
        LONGDESC = "Promote the dummy service to the master mode"
        SHORTDESC = "Promote service"

    class OCFHandler_demote(Handler):
        LONGDESC = "Demote the dummy service from the master mode"
        SHORTDESC = "Demote service"

    class OCFHandler_notify(Handler):
        LONGDESC = "Notify the dummy service if the master status changes"
        SHORTDESC = "Notify service"

    class OCFHandler_migrate_to(Handler):
        LONGDESC = "Ask the dummy service to migrate to the other node"
        SHORTDESC = "Migrate service to node"

    class OCFHandler_migrate_from(Handler):
        LONGDESC = "Ask the dummy service to migrate from the other node"
        SHORTDESC = "Migrate service from node"

    ###########################################################################

    def handler_promote(self):
        self.lock.create_file('master')
        self.lock.create()
        self.exit.success('The agent was promoted')

    def handler_demote(self):
        self.lock.remove_file('master')
        self.lock.create()
        self.exit.success('The agent was demoted')

    def handler_start(self):
        self.lock.create()
        self.exit.success('The agent was started')

    def handler_stop(self):
        self.lock.remove()
        self.exit.success('The agent was stopped')

    def handler_monitor(self):
        if self.lock.file_is_present('master'):
            self.exit.running_master('The agent is running in the master mode')
        if self.lock.is_present:
            self.exit.success('The agent is running')
        self.exit.not_running('The agent is not running')

    def handler_reload(self):
        self.lock.create()
        self.exit.success('The agent was reloaded')

    def handler_notify(self):
        self.lock.create()
        self.exit.success('The agent was notified')

    def handler_migrate_to(self):
        self.lock.remove()
        self.exit.success('The agent will migrate to')

    def handler_migrate_from(self):
        self.lock.create()
        self.exit.success('The agent will migrate from')


###############################################################################

if __name__ == "__main__":
    ocf = DummyOCF()
    ocf.call()

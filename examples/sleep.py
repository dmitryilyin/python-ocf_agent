#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ocf_agent.agent import Agent
from ocf_agent.parameter import StringParameter
from ocf_agent.handler import Handler
from ocf_agent.handler import MonitorHandler


class SleepOCF(Agent):
    VERSION = "1.0"
    LOCK_DIR = '/tmp'
    PID_DIR = '/tmp'
    SHORTDESC = "Sleep test OCF agent"
    LONGDESC = "This OCF agent can run 'sleep' command as a daemon"
    LOG_HANDLERS = ['console']

    # PARAMETERS #

    class OCFParameter_time(StringParameter):
        DEFAULT = '10000'
        LONGDESC = "How long the sleep process should work"
        SHORTDESC = "Sleep time"

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

    ###########################################################################

    COMMAND = 'sleep'

    @property
    def is_running(self):
        return self.process.is_running(self.pid.number)

    def handler_start(self):
        if self.is_running:
            self.exit.success(
                'Process is already running with pid: "%s"' % (
                    self.pid.number,
                )
            )

        process = self.process.daemonize(
            self.COMMAND,
            self.param('time')
        )
        pid = process.pid
        self.pid.create(pid)
        self.exit.success(
            'Process started with pid: "%s" pid_file "%s"!' % (
                pid,
                self.pid.path,
            )
        )

    def handler_stop(self):
        if not self.is_running:
            self.exit.success('Process is already not running!')

        pid = self.pid.number
        result = self.process.ensure_terminate(pid)

        if result:
            self.pid.remove()
            self.exit.success(
                'Process: "%s" have been stopped!' % (
                    pid,
                )
            )

        self.exit.error_generic(
            'Process: "%s" have FAILED to stop!' % (
                pid,
            )
        )

    def handler_monitor(self):
        if not self.pid.present:
            self.exit.not_running(
                'There is no pid_file: "%s". Service is not running!' % (
                    self.pid.path
                )
            )

        if not self.is_running:
            self.exit.not_running(
                'Pid_file: "%s" is present with pid: "%s" '
                'but the service is not running' % (
                    self.pid.path,
                    self.pid.number,
                )
            )

        self.exit.success(
            'Process is running with pid: "%s"' % self.pid.number
        )

        #######################################################################


if __name__ == "__main__":
    ocf = SleepOCF()
    ocf.call()

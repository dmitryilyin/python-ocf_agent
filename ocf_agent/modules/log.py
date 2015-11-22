# -*- coding: utf-8 -*-
import logging
import os
import sys
from logging.handlers import SysLogHandler
from ocf_agent import constants


class Log(object):
    """
    The Logger object is a wrapper of the Python's logger class.
    It can create a configured Logger object and use it to log messages.
    """
    def __init__(self, agent):
        """
        The Log object requires the Agent object as the first argument.

        :param agent: Parent Agent.
        :type agent: Agent
        """
        self.agent = agent

    @property
    def logger(self):
        """
        Returns the configured Logger class instance. It can be used by
        logging methods or can be used directly.

        :return: Logger object
        :rtype: Logger
        """
        logger = logging.getLogger(self.tag)
        logger.level = self.level
        logger.handlers = []
        if 'console' in self.enabled_handlers:
            logger.handlers.append(self.handler_console)
        if 'syslog' in self.enabled_handlers:
            logger.handlers.append(self.handler_syslog)
        if 'file' in self.enabled_handlers:
            logger.handlers.append(self.handler_file)
        return logger

    @property
    def enabled_handlers(self):
        """
        Get the list of enabled handler types

        :return: List of handler names
        :rtype: list
        """
        return getattr(
            self.agent,
            constants.CONST_HANDLERS,
            constants.DEFAULT_LOG_HANDLERS,
        )

    @property
    def level(self):
        """
        Returns the current maximum log level. Debug mode can be enabled
        if the pacemaker sends the debug environment variable.

        :return: Debug level
        :rtype: int
        """
        if self.agent.environment.is_debug:
            return logging.DEBUG
        else:
            return logging.INFO

    @property
    def tag(self):
        """
        Returns the log tag. It's used as the Logger object name to mark
        the process which have emitted the message.

        :return: Log Tag
        :rtype: str
        """
        tag = self.agent.environment.res_instance
        if self.agent.action:
            tag += '[%s]' % self.agent.action
        return tag

    @property
    def log_file_path(self):
        """
        Path to the log file. Used by the 'file' handler.

        :return: Path to log file
        :rtype: str
        """
        log_file = self.agent.environment.instance_name
        if self.agent.environment.instance_suffix:
            log_file += '_' + self.agent.environment.instance_suffix
        log_file += '.log'
        return os.path.join(constants.LOG_FILE_DIRECTORY, log_file)

    # log formats #

    @property
    def format_date(self):
        """
        Date format string

        :rtype: str
        """
        return '%Y-%m-%d %H:%M:%S'

    @property
    def format_date_prefix(self):
        """
        Date prefix of the log message. It will be used by console and
        log handlers to mark the message time and date.

        :type: str
        """
        return '%(asctime)s.%(msecs)03d'

    @property
    def format_suffix(self):
        """
        Log message suffix. The body part of the log message.

        :rtype: str
        """
        return '%(name)s %(levelname)s %(message)s'

    @property
    def formatter_file(self):
        """
        The formatter with the date prefix. Used for file and console logger.

        :return: Formatter object
        :rtype: Formatter
        """
        file_format = '%s %s' % (
            self.format_date_prefix,
            self.format_suffix,
        )
        return logging.Formatter(file_format, self.format_date)

    formatter_console = formatter_file

    @property
    def formatter_syslog(self):
        """
        The Syslog formatter does not send the date prefix.

        :return: Formatter object
        :rtype: Formatter
        """
        return logging.Formatter(self.format_suffix)

    # log handlers #

    @property
    def handler_console(self):
        """
        The Console handler sends the messages to the standard error output.

        :return: Console Handler
        :rtype: Handler
        """
        handler = logging.StreamHandler(
            stream=sys.stderr,
        )
        handler.setFormatter(self.formatter_console)
        return handler

    @property
    def handler_file(self):
        """
        The File handler sends the messages directly to a log file.

        :return: File Handler
        :rtype: Handler
        """
        handler = logging.FileHandler(
            filename=self.log_file_path,
            encoding=self.agent.encoding,
        )
        handler.setFormatter(self.formatter_file)
        return handler

    @property
    def handler_syslog(self):
        """
        The Syslog handler sends the messages to the syslog service.

        :return: Syslog Handler
        :rtype: Handler
        """
        handler = SysLogHandler(
            address=constants.SYSLOG_SOCKET,
            facility=self.agent.environment.log_facility,
        )
        handler.setFormatter(self.formatter_syslog)
        return handler

    # logging methods #

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    warn = warning

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    err = error

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    crit = critical

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)

    @staticmethod
    def output(msg):
        """
        Directly write the message to the standard output.

        :param msg: Text
        :type: msg: str
        """
        sys.stdout.write(msg)

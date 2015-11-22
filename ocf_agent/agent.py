# -*- coding: utf-8 -*-

import sys
from ocf_agent import constants
from ocf_agent.helpers import docstring_format
from ocf_agent.helpers import memoization
from ocf_agent.modules.environment import Environment
from ocf_agent.modules.exit import Exit
from ocf_agent.modules.handlers import Handlers
from ocf_agent.modules.lock import Lock
from ocf_agent.modules.pid import Pid
from ocf_agent.modules.process import Process
from ocf_agent.modules.log import Log
from ocf_agent.modules.metadata import MetaData
from ocf_agent.modules.parameters import Parameters


class Agent(object):
    _action = None

    @property
    @docstring_format(constants.CONST_NAME)
    def name(self):
        """
        Name of this OCF agent. It's either taken from the class name
        or can be manually set by the *{0}* constant.

        :return: The agent name
        :rtype: str
        """
        return getattr(
            self,
            constants.CONST_NAME,
            self.__class__.__name__,
        )

    @property
    @docstring_format(constants.CONST_VERSION, constants.DEFAULT_VERSION)
    def version(self):
        """
        The agent's version number. Can be set by the *{0}* constant or will
        default to **{1}**.

        :return: The agent version
        :rtype: str
        """
        return getattr(
            self,
            constants.CONST_VERSION,
            constants.DEFAULT_VERSION,
        )

    @property
    @docstring_format(constants.CONST_SHORT_DESCRIPTION)
    def short_description(self):
        """
        Short description string of this agent. Can be manually set by the
        *{0}* constant. Will default to name if not set.

        :return: Agent's short description
        :rtype: str
        """
        return getattr(
            self,
            constants.CONST_SHORT_DESCRIPTION,
            self.name,
        )

    @property
    @docstring_format(constants.CONST_LONG_DESCRIPTION)
    def long_description(self):
        """
        Long description string of this agent. Can be manually set by
        the *{0}* constant. Will default to the short description unless
        defined.

        :return: Agent's long description
        :rtype: str
        """
        return getattr(
            self,
            constants.CONST_LONG_DESCRIPTION,
            self.short_description,
        )

    @property
    @docstring_format(constants.CONST_LANGUAGE, constants.DEFAULT_LANGUAGE)
    def language(self):
        """
        The language reported by this agent in its metadata XML.
        It can be manually set by the *{0}* constant and will return the
        default value **{1}** if not defined.

        :return: The agent's language
        :rtype: str
        """
        return getattr(
            self,
            constants.CONST_LANGUAGE,
            constants.DEFAULT_LANGUAGE,
        )

    @property
    @docstring_format(constants.CONST_ENCODING, constants.DEFAULT_ENCODING)
    def encoding(self):
        """
        Returns the encoding used by this agent in its metadata and logging.
        Can be manually defined be the *{0}* constant or will use the
        default value **{1}**.

        :return: Agent's encoding
        :rtype: str
        """
        return getattr(
            self,
            constants.CONST_ENCODING,
            constants.DEFAULT_ENCODING,
        )

    @property
    def action(self):
        """
        Returns the action name the OCF have been called with or the
        manually defined action. The action will be used to determine which
        handler should be run. Returns None if no action was defined.

        :return: The defined action
        :rtype: str or None
        """
        if self._action is not None:
            return self._action
        if len(sys.argv) >= 2:
            action = sys.argv[1]
            self.action = action
        return self._action

    @action.setter
    def action(self, value=None):
        """
        Manually sets the resource agent's action

        :type value: str
        :param value: The action name
        """
        if value is None:
            self._action = None
            return
        if value in constants.ALIAS_HANDLERS:
            value = constants.ALIAS_HANDLERS[value]
        self._action = value

    def call(self, action=None):
        """
        Call the agent with defined action. It will try to find a handler
        function for this action and run it.

        :param action: Run with this action
        :type action: str
        """
        if action:
            self.action = action
        self.validate()
        if self.action == 'validate-all':
            self.exit.success('Validation successful')
        if self.action == "meta-data":
            self.metadata.show()
            self.exit.success('Metadata output')
        if self.action == 'usage':
            self.usage()
            self.exit.success('Usage output')
        self.handlers.current()

    __call__ = call

    def validate(self):
        """
        Validate the agent's configuration and the configuration of all
        the agent's handlers and parameters. Agent will validate itself first,
        and then run the validate methods of other objects.
        """
        if self.action is None:
            self.usage()
            self.exit.error_arguments('No action specified')
        if self.action not in self.handlers.actions:
            self.usage()
            self.exit.error_unimplemented(
                "Specified action: '%s' is neither a built-in "
                "nor a defined action" % self.action
            )

        self.parameters.validate()
        self.handlers.validate()

    def usage(self):
        """
        Prints the agent's usage information including all implemented handlers
        """
        self.log.output(
            "usage: %s {%s}\n" % (
                self.name,
                "|".join(self.handlers.actions)
            )
        )

    def param(self, name):
        """
        Shortcut to get a parameter value by its name. Returns None
        if the parameter is not found.

        :param name: Parameter name
        :type name: str
        :return: Parameter value
        :rtype: str or int or bool or None
        """
        return self.parameters.value(name)

    ###########################################################################

    @property
    @memoization
    def exit(self):
        """
        The Exit object handles different exit conditions, exit codes
        and logging.

        :return: The Exit object
        :rtype: Exit
        """
        return Exit(self)

    @property
    @memoization
    def parameters(self):
        """
        Agent's parameters object. It deals with parameter collection, values
        defaults, types and validation.

        :return: The parameters object
        :rtype: Parameters
        """
        return Parameters(self)

    @property
    @memoization
    def handlers(self):
        """
        Returns the handlers object. It's responsible for handlers gathering,
        processing their attributes, choosing the right handler for an action
        and running the handler function.

        :return: The handlers object
        :rtype: Handlers
        """
        return Handlers(self)

    @property
    @memoization
    def environment(self):
        """
        The environment object does everything related to the environment
        variables passed from the cluster. It can collect and retrieve many
        predefined values.

        :return: The environment object
        :rtype: Environment
        """
        return Environment(self)

    env = environment

    @property
    @memoization
    def log(self):
        """
        The Log object handles all agent's logging and output functions.
        It can control where dies the logging go, the log level and
        log formats.

        :return: The log object
        :rtype: Log
        """
        return Log(self)

    @property
    @memoization
    def metadata(self):
        """
        The Metadata object can generate the metadata XML that is required to
        report the agents capabilities to the cluster.

        :return: the metadata object
        :rtype: MetaData
        """
        return MetaData(self)

    @property
    @memoization
    def lock(self):
        """
        The Lock object can work with lock files. It can create lock file
        for this agent with or without custom key, check if they are present
        and remove them.

        :return: The lock object
        :rtype: Lock
        """
        return Lock(self)

    @property
    @memoization
    def pid(self):
        """
        The Pid object can work with pid files. It can create pid file
        for this agent with or without custom key, check if they are present,
        read and remove pid files either created by the service or by the
        agent.

        :return: The pid object
        :rtype: Pid
        """
        return Pid(self)

    @property
    @memoization
    def process(self):
        """
        The Process object can run processes, inspect the process list
        and send signals to a process.

        :return: The process object
        :rtype: Process
        """
        return Process(self)

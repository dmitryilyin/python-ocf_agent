from ocf_agent import constants
from ocf_agent.helpers import docstring_format
from ocf_agent.helpers import memoization
from ocf_agent.helpers import string_to_integer


class Handler(object):
    """
    The Handler object represents an action OCF agent can be called with.
    It can process the action's attributes and select the agent's handler
    method to run.
    """
    _action = None

    def __init__(self, handlers=None):
        """
        The Handler object should be created with the parent Handlers object as
        the first argument.

        :param handlers: Parent Handlers object
        :type handlers: Handlers
        """
        self.handlers = handlers
        self.agent = self.handlers.agent

    def validate(self):
        """
        Validate if this Handler object is configured correctly.
        """
        if not self.__class__.__name__.startswith(
                constants.HANDLER_CLASS_PREFIX
        ):
            self.agent.exit.error_configuration(
                "ResourceHandler class '%s' name does not start with '%s'" %
                (self.__class__.__name__, constants.HANDLER_CLASS_PREFIX)
            )

    @property
    @docstring_format(constants.CONST_ACTION)
    def action(self):
        """
        Returns the action of this handler. Action is determined either by the
        handler's class name after the prefix or manually by the *{0}*
        constant.
        Action is used to select the agent's handler method to run when this
        object is called.

        :return: Handler action
        :rtype: str
        """
        if self._action is not None:
            return self._action
        if hasattr(self, constants.CONST_ACTION):
            action = getattr(self, constants.CONST_ACTION)
        else:
            action = str(
                self.__class__.__name__[len(constants.HANDLER_CLASS_PREFIX):]
            )
            if action.startswith('monitor_'):
                action = action.split('_')[0]
        self._action = action
        return self._action

    name = action
    full_name = action

    @property
    def attribute_names(self):
        """
        Returns the list of attributes that are meaningful for this handler.
        They are used to assemble actions in the meta-data xml.
        :return: list of attribute names
        :rtype: list
        """
        return ['name', 'timeout']

    @property
    @memoization
    def attributes(self):
        """
        Returns the dictionary of attribute names and their values.

        :return: Attribute names and values
        :rtype: dict
        """
        attributes = {}
        for attribute_name in self.attribute_names:
            attribute_value = getattr(self, attribute_name, None)
            if attribute_value is not None:
                attributes[attribute_name] = attribute_value
        return attributes

    @property
    @docstring_format(constants.CONST_SHORT_DESCRIPTION)
    def short_description(self):
        """
        Short description string of this handler. Can be defined by the *{0}*
        constant or will default to the handler's action.
        This value is not actually used anywhere but can be used for reference.

        :return: Short description string
        :rtype: str
        """
        return getattr(
            self,
            constants.CONST_SHORT_DESCRIPTION,
            self.action
        )

    @property
    @docstring_format(constants.CONST_LONG_DESCRIPTION)
    def long_description(self):
        """
        Long description of this handler. Can be defined by the
        *{0}* constant or will default to the short description.
        This value is not actually used anywhere but can be used for reference.

        :return: Long description
        :rtype: str
        """
        return getattr(
            self,
            constants.CONST_LONG_DESCRIPTION,
            self.short_description
        )

    @property
    @docstring_format(constants.CONST_LANGUAGE, constants.DEFAULT_LANGUAGE)
    def language(self):
        """
        The handler's description language. Can be set by the *{0}* constant
        or will default to the default value **{1}**.
        :return:
        """
        return getattr(
            self,
            constants.CONST_LANGUAGE,
            constants.DEFAULT_LANGUAGE
        )

    @property
    @docstring_format(constants.CONST_METHOD)
    def default_method_name(self):
        """
        This is the name of the agent's handler method called by this handler
        if no other method name is defined by the *{0}* constant.

        :return: Default handler method name
        :rtype: str
        """
        return constants.OCF_HANDLER_METHOD_PREFIX + str(self.full_name)

    @property
    @docstring_format(constants.CONST_METHOD)
    def method_name(self):
        """
        The handler will try to find this method in the Agent object and
        call it when the Handler object is called. Can be defined by the *{0}*
        constant or will be set to the default method name.

        :return: Handler's method name
        :rtype: str
        """
        return getattr(
            self,
            constants.CONST_METHOD,
            self.default_method_name
        )

    @property
    def method(self):
        """
        Returns the Agent's method object associated with this handler.
        Will return None if the method is not found.

        :return: The Agent's handler method.
        :rtype: func or None
        """
        return getattr(self.handlers.agent, self.method_name, None)

    def call(self):
        """
        When the Handler object is called it will try to find Agent's handler
        method and call it. If there is no such method the agent will
        exit with error message.
        """
        if self.method is not None and hasattr(self.method, '__call__'):
            self.method()
        else:
            self.agent.exit.error_unimplemented(
                "Agent does not have method: '%s'" % self.method_name
            )

    __call__ = call

    @property
    @memoization
    @docstring_format(constants.CONST_TIMEOUT, constants.DEFAULT_TIMEOUT)
    def timeout(self):
        """
        Returns the handler's timeout value. It will be used in the meta-data
        XML to advise the user what is the minimal number of seconds required
        to execute this agent's action.
        The value can be set by the *{0}* constant and will default to the
        default value **{1}** if not set.

        :return: The timeout value in seconds
        :rtype: int
        """
        return string_to_integer(
            getattr(
                self,
                constants.CONST_TIMEOUT,
                constants.DEFAULT_TIMEOUT
            )
        )


###############################################################################


class MonitorHandler(Handler):
    """
    MonitorHandler extends the Handler object with several properties that
    only monitor actions have.
    """

    @property
    def attribute_names(self):
        """
        MonitorHandler has all the properties of the Handler object and
        additional ones.

        :return: List of attributes
        :rtype: list
        """
        return super(MonitorHandler, self).attribute_names + [
            'interval', 'depth', 'role']

    @property
    @memoization
    @docstring_format(constants.CONST_INTERVAL, constants.DEFAULT_INTERVAL)
    def interval(self):
        """
        Interval is the number of seconds between the monitor actions calls.
        This value is used in the meta-data XML to advise the user what is the
        minimum interval for this monitor? or for this monitor type if there
        are several monitor actions defined.
        Interval can be set by the *{0}* constant and will default to **{1}**
        if unset.

        :return: The interval value in seconds
        :rtype: int
        """
        return string_to_integer(
            getattr(
                self,
                constants.CONST_INTERVAL,
                constants.DEFAULT_INTERVAL,
            )
        )

    @property
    @memoization
    @docstring_format(constants.CONST_DEPTH, constants.DEFAULT_DEPTH)
    def depth(self):
        """
        Depth, or the check_level, is used to define several monitor actions.
        For example, the short monitor action with a small depth number and
        the long and expensive one with a large depth. Small monitor can have
        a small interval value and be called very often and the large monitor
        can perform many additional checks, have a large monitor value and be
        called infrequently. The depth value will be used to distinguish these
        actions.
        Depth can be set by the *{0}* constant and will default to **{1}**
        if unset.

        :return: The depth value
        :rtype: int
        """
        return string_to_integer(
            getattr(
                self,
                constants.CONST_DEPTH,
                constants.DEFAULT_DEPTH,
            )
        )

    @property
    @memoization
    @docstring_format(constants.CONST_ROLE)
    def role(self):
        """
        Role can be used to tell if this monitor action should be run only on
        the master instance in a multi-state configuration, only on a slave one
        or or any instance.
        The value can be Master, Slave or None.
        Role can be set by the *{0}* constant and will default to **None**.

        :return: The role value
        :rtype: str or None
        """
        role = getattr(
            self,
            constants.CONST_ROLE,
            None
        )
        if role is None:
            return None
        else:
            role = str(role).lower().capitalize()
        return role

    @property
    @memoization
    def full_name(self):
        """
        Full name of this handler.
        It will ne equal to the name for a non-monitor handler and will
        contain depth and role for a monitor action.
        Full name is used to find the Agent's handler method.

        :return: Handler's full name
        :rtype: str
        """
        full_name = self.action
        if self.role is not None:
            full_name += '_' + self.role.lower()
        if self.depth is not None and self.depth != 0:
            full_name += '_' + str(self.depth)
        return full_name

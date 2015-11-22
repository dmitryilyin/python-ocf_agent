# -*- coding: utf-8 -*-
from ocf_agent import constants
from ocf_agent.helpers import memoization


class Handlers(object):
    """
    The Handlers object is a collection of handler objects.
    It can collect then and work with their attributes.
    """

    def __init__(self, agent):
        """
        The Handlers object should be created with the parent Agent object
        as the first argument.

        :param agent: Parent Agent object
        :type agent: Agent
        """
        self.agent = agent

    @property
    @memoization
    def handlers(self):
        """
        Returns the list of defined Handler instances

        :rtype: list
        :return: The list of Handler objects
        """
        handlers = []
        for entry in dir(self.agent):
            if not entry.startswith(constants.HANDLER_CLASS_PREFIX):
                continue
            handler_class = getattr(self.agent, entry)
            handler_class_instance = handler_class(self)
            handlers.append(handler_class_instance)
        return handlers

    all = handlers
    __call__ = handlers

    @property
    @memoization
    def actions(self):
        """
        Returns a set of all implemented Handler actions

        :rtype: set
        :return: Set of implemented action names
        """
        defined_handlers = set(
            [
                handler.action for handler in self.handlers
                ]
        )
        defined_handlers.update(constants.BUILTIN_HANDLERS)
        defined_handlers.update(constants.ALIAS_HANDLERS.keys())
        return defined_handlers

    @property
    def current(self):
        """
        Find the current Handler instance using the Agent's action value and
        check\_level for a monitor action. Raises error if the handler is
        not found.

        :return: The current Handler
        :rtype: Handler
        """
        handler = self.get(
            action=self.agent.action,
            check_level=self.agent.environment.check_level,
        )
        if handler is not None:
            return handler
        self.agent.exit.error_unimplemented(
            "Handler for action '%s' is not found" % self.agent.action
        )

    def get(self, action, check_level=None):
        """
        Try to get a Handler instance by its name and, for a monitor action,
        by its check level. Returns None if the instance is not found.

        :param action: Action name
        :type action: str
        :param check_level: Monitor check level
        :type check_level: int or None
        :return: The Handler instance
        :rtype: Handler of None
        """
        if action == 'monitor' and check_level is not None:
            matcher_handlers = [
                handler for handler in self.handlers if
                handler.action == action and
                handler.depth == check_level
                ]
            if matcher_handlers:
                return matcher_handlers[0]
            else:
                return self.get(action)
        else:
            matched_handlers = [
                handler for handler in self.handlers
                if handler.action == action
                ]
            if matched_handlers:
                return matched_handlers[0]
            return None

    @property
    @memoization
    def attributes(self):
        """
        Return the dictionary of all Handler full names and their
        attributes.

        :return: Dictionary of handler full names and attributes.
        :rtype: dict
        """
        attributes = {}
        for handler in self.handlers:
            attributes[handler.full_name] = handler.attributes
        return attributes

    def validate(self):
        """
        Validate if the handlers are configured correctly.
        """
        for handler in self.handlers:
            handler.validate()

# -*- coding: utf-8 -*-
from ocf_agent import constants
from ocf_agent.helpers import memoization


class Parameters(object):
    """
    The Parameters object is a collection of Parameter objects.
    It can collect Parameters and work with their values.
    """

    def __init__(self, agent):
        """
        The Parameters object should be created with the parent Agent
        object as the first argument.

        :param agent: Parent Agent object
        :type agent: Agent
        """
        self.agent = agent

    @property
    @memoization
    def parameters(self):
        """
        Returns the dictionary of all defined parameter names
        and their object instances.

        :rtype: dict
        :return: Dictionary of parameter names and objects
        """
        parameters = {}
        for entry in dir(self.agent):
            if not entry.startswith(constants.PARAMETER_CLASS_PREFIX):
                continue
            parameter_class = getattr(self.agent, entry)
            parameter_class_instance = parameter_class(self)
            parameters[parameter_class_instance.name] = \
                parameter_class_instance
        return parameters

    all = parameters
    __call__ = parameters

    def get(self, name):
        """
        Get the parameter instance by its name.

        :param name: Parameter name
        :type name: str
        :return: Parameter instance
        :type: Parameter or None
        """
        if name in self.parameters:
            return self.parameters[name]
        return None

    def value(self, name):
        """
        Get the parameter value by the parameter name.

        :param name: Parameter name
        :type name: str
        :return: Parameter value
        :rtype: int or boot or str or None
        """
        parameter = self.get(name)
        if parameter is None:
            return None
        return parameter.value

    @property
    def values(self):
        """
        Get a dictionary of parameter names and their values.

        :return: Parameter name and values
        :rtype: dict
        """
        values = {}
        for parameter_name, parameter in self.parameters.items():
            values[parameter_name] = parameter.value
        return values

    def validate(self):
        """
        Validate if the parameters are configured correctly.
        """
        for parameter in self.parameters.values():
            parameter.validate()

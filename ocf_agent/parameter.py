# -*- coding: utf-8 -*-

import os
from ocf_agent import constants
from ocf_agent.helpers import docstring_format
from ocf_agent.helpers import memoization
from ocf_agent.helpers import string_to_bool
from ocf_agent.helpers import string_to_integer


class BaseParameter(object):
    def __init__(self, parameters=None):
        """
        A parameter should be created with its parent Parameters
        object provided ans the first argument.

        :param parameters: The parent parameters object
        :type parameters: Parameters
        """
        self.parameters = parameters
        self.agent = self.parameters.agent
        self._value = None

    def validate(self):
        """
        Validate if this Parameter object is configured correctly
        """
        if not self.__class__.__name__.startswith(
                constants.PARAMETER_CLASS_PREFIX
        ):
            self.agent.exit.error_configuration(
                "ResourceParameter class name does not start with '%s'" %
                constants.PARAMETER_CLASS_PREFIX
            )

    @property
    @docstring_format(constants.CONST_NAME)
    def name(self):
        """
        The parameter's name can be taken from the parameter class' name
        or manually defined in the parameter class by the *{0}* constant.

        :return: Parameter's name
        :rtype: str
        """
        if hasattr(self, constants.CONST_NAME):
            name = getattr(
                self,
                constants.CONST_NAME
            )
        else:
            name = str(
                self.__class__.__name__[len(constants.PARAMETER_CLASS_PREFIX):]
            )
        return name

    @property
    @docstring_format(constants.CONST_SHORT_DESCRIPTION)
    def short_description(self):
        """
        Short description of this parameter. Will default to the parameter's
        name unless defined by the *{0}* constant.

        :return: Short description
        :rtype: str
        """
        return getattr(
            self,
            constants.CONST_SHORT_DESCRIPTION,
            self.name
        )

    @property
    @docstring_format(constants.CONST_LONG_DESCRIPTION)
    def long_description(self):
        """
        Long description of this parameter. It will be taken from the constant
        *{0}* in the parameter's class or will default to the short
        description.

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
        The description language reported by this parameter. Will use the
        value defined by the *{0}* constant or the default value **{1}**.

        :return: Parameter language
        :rtype: str
        """
        return getattr(
            self,
            constants.CONST_LANGUAGE,
            constants.DEFAULT_LANGUAGE
        )

    @property
    def type(self):
        """
        Returns the Python type which the value of this parameter should
        belong to. This method should be redefined by the inherited classes.

        :return: Expected type of the value
        """
        self.agent.exit.error_unimplemented(
            '%s is an abstract class and cannot be used directly' %
            self.__class__.__name__
        )

    @property
    def type_name(self):
        """
        Returns the string name of the expected type

        :rtype: str
        :return: Type name
        """
        if self.type is int:
            return "integer"
        if self.type is str:
            return "string"
        if self.type is bool:
            return "boolean"

    @property
    @memoization
    @docstring_format(constants.CONST_DEFAULT)
    def default(self):
        """
        The default value of this parameter. Can be defined by the *{0}*
        constant inside the parameter class definition.

        :return: The default value
        :rtype: bool or str or int
        """
        return self.process_value(
            getattr(
                self,
                constants.CONST_DEFAULT,
                None)
        )

    @property
    def value(self):
        """
        Returns this parameter's value. It will try to take the already
        defined value. Then the value will be taken from the
        corresponding environment variable, and, finally, the
        default value will be returned.

        :return: The parameter's value of the default value
        :rtype: bool or str or int
        """
        if self._value is not None:
            return self._value
        if self.env_variable_name in os.environ:
            self.value = os.environ[self.env_variable_name]
        if self._value is not None:
            return self._value
        return self.default

    @value.setter
    def value(self, new_value):
        """
        Manually set the current parameter value and run the value processing.

        :param new_value: The new value
        :type new_value: object
        """
        self._value = self.process_value(new_value)

    @property
    @memoization
    @docstring_format(constants.CONST_UNIQUE)
    def unique(self):
        """
        Indicates that this value is unique across the cluster.
        If there are several resources of this type, a single value
        can be assigned only to a single instance and other instances
        should have different values.
        If disabled, many similar resources may have the same value of
        this parameter.
        Can be set by the *{0}* constant in the parameter definition
        and can be either True or False. Defaults to **False**.

        :rtype: bool
        :return: true or false
        """
        return string_to_bool(
            getattr(self, constants.CONST_UNIQUE, False)
        )

    @property
    @memoization
    @docstring_format(constants.CONST_REQUIRED)
    def required(self):
        """
        Indicates that this value is required to use this resource and
        a user should provide an explicit value for this parameter.
        Default value will nod be used.
        Can ne set by the *{0}* constant in the parameter definition
        and can be either true or False. Defaults to **False**.

        :rtype: bool
        :return: true or false
        """
        return string_to_bool(
            getattr(self, constants.CONST_REQUIRED, False)
        )

    @property
    def env_variable_name(self):
        """
        The environment variable name used to pass the value
        of this parameter from the cluster configuration.

        :rtype: str
        :return: The environment variable name
        """
        return constants.VAR_PARAMETER_PREFIX + self.name

    def process_value(self, value):
        """
        Called modify and validate function to import a new data
        either for the default of for the current parameter value.

        :type value: object
        :param value: a new value
        :rtype: object
        :return: processed value
        """
        value = self.modify_value(value)
        if not self.validate_value(value):
            self.parameters.agent.exit.error_arguments(
                "The value: '%s' of the parameter: '%s' is not correct!" % (
                    value, self.name))
        return value

    def validate_value(self, value):
        """
        Validates the value of this parameter. This function
        can be redefined by a child class if you need to validate
        a specific value type. Returns true if value passes the test.

        :type value: object
        :param value: a new value
        :rtype: bool
        :return: true or false
        """
        if value is None:
            return True
        return isinstance(value, self.type)

    def modify_value(self, value):
        """
        This function is used to somehow modify the new value.
        It should be redefined by a child class for a specific
        action. Does nothing by default.

        :type value: object
        :param value: the new value
        :rtype: object
        :return: the modified value
        """
        return value


###############################################################################


class StringParameter(BaseParameter):
    @property
    def type(self):
        """
        Type of the String property

        :return: string type
        """
        return str

    def modify_value(self, value):
        """
        String provider does not chencge the input value keeping
        it as a string.

        :param value: input value
        :type value: object
        :return: modified value
        :rtype: str
        """
        if value is None:
            return value
        return str(value)


###############################################################################


class IntegerParameter(BaseParameter):
    @property
    def type(self):
        """
        Type of the Integer property

        :return: integer type
        """
        return int

    def modify_value(self, value):
        """
        Integer property converts ins value to an integer
        or to None if input value cannot be converted.

        :param value: input value
        :type value: str
        :return: integer value
        """
        return string_to_integer(value)


###############################################################################


class BooleanParameter(BaseParameter):
    @property
    def type(self):
        """
        Type of the Boolean property

        :return: boolean type
        """
        return bool

    def modify_value(self, value):
        """
        Boolean property converts its value to boolean or to None
        if the value cannot be converted.

        :param value: input value
        :type value: str
        :return: boolean value
        :rtype: bool
        """
        return string_to_bool(value)

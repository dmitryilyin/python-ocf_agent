# -*- coding: utf-8 -*-

from ocf_agent import constants


def string_to_bool(value, default=None):
    """
    Convert a string value to boolean with
    different possible true and false variants and
    the default value option if conversion was not successful.

    :param value: Input value
    :type value: str
    :param default: Optional default value
    :type default: object
    :return: true, false, or the default value
    :rtype: True or False or None
    """
    if value is None or isinstance(value, bool):
        return value
    if str(value).lower() in constants.VALUES_TRUE:
        return True
    if str(value).lower() in constants.VALUES_FALSE:
        return False
    return default


def string_to_integer(value, default=None):
    """
    Convert a string value to an integer value stripping non-numeric
    letters and with optional default value if conversion was not successful.

    :param value: Input value
    :type value: str
    :param default: Optional default value
    :type default: object
    :return: Integer value or the default value
    :rtype: int or None
    """
    if value is None:
        return None
    try:
        return abs(int(value))
    except (ValueError, TypeError):
        pass
    try:
        value = ''.join([letter for letter in str(value) if letter.isdigit()])
        return abs(int(value))
    except (ValueError, TypeError):
        return default


def memoization_prepare(self):
    """
    Prepare the memoization structure in the class
    """
    if not isinstance(
            getattr(self, constants.CONST_MEMOIZATION, None),
            dict,
    ):
        setattr(self, constants.CONST_MEMOIZATION, {})


def memoization_set(self, key, value):
    """
    Set the new value to the memoization structure

    :param self: Class self object
    :param key: Property name
    :type key: str
    :param value: Property value
    :type value: object
    """
    memoization_prepare(self)
    getattr(self, constants.CONST_MEMOIZATION, {})[key] = value
    return value


def memoization_get(self, key):
    """
    Retrieve the stored memoization value

    :param self: Class self object
    :param key: Property name
    :type key: str
    """
    memoization_prepare(self)
    return getattr(self, constants.CONST_MEMOIZATION, {}).get(key, None)


def memoization(function):
    """
    Property memoization decorator.

    Saves the first property function output value and returns the saved
    value when the property function is called again. Should be used only
    for a property method or a method without arguments. Property decorator
    should be applied after this one.

    :param function: Property function
    :type function: func
    :return: Decorated property function
    :rtype: func
    """

    def _decorator_(self):
        key = function.__name__
        value = memoization_get(self, key)
        if value is not None:
            return value
        else:
            value = function(self)
            memoization_set(self, key, value)
            return value

    _decorator_.__doc__ = function.__doc__
    return _decorator_


def docstring_format(*values):
    """
    This decorator can be used to replace placeholders in a method docstring
    with variable or constant values. It allows using variables in a
    method docstring. It also screen all underscore characters to be
    processed correctly by Sphinx.

    :param values A list of substitute values
    :type values: list
    :return: Method with formatted docstring
    :rtype: func
    """

    def _decorator_(function):
        function.__doc__ = function.__doc__.format(*values).replace('_', '\_')
        return function

    return _decorator_

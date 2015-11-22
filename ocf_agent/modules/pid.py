# -*- coding: utf-8 -*-

import os
from ocf_agent import constants
from ocf_agent.helpers import docstring_format
from ocf_agent.helpers import string_to_integer


class Pid(object):
    """
    The Pid object can create, check, read and remove pid files.
    """

    def __init__(self, agent):
        """
        The Pid object should have the Agent object as the first argument.

        :param agent: The parent Agent
        :type agent: Agent
        """
        self.agent = agent

    @property
    @docstring_format(constants.CONST_PID_DIR, constants.DEFAULT_PID_DIR)
    def directory(self):
        """
        The directory where all the pid files will be placed.
        Can be set by the *{0}* constant in the Agent class
        and will default to **{1}**.

        :return: Pid file directory
        :rtype: str
        """
        return getattr(
            self.agent,
            constants.CONST_PID_DIR,
            constants.DEFAULT_PID_DIR,
        )

    def file_name(self, key=None):
        """
        The pid file name for this agent.  with the custom key if the key is
        provided.

        :param key: Custom pid file suffix
        :type key: str or None
        :return: Pid file name
        :rtype: str
        """
        file_name = self.agent.name
        if self.agent.environment.res_instance is not None:
            file_name += '-' + self.agent.environment.res_instance
        if key is not None:
            file_name += '-' + key
        return file_name + '.pid'

    @docstring_format(constants.CONST_PID_FILE)
    def file_path(self, key=None):
        """
        The full path to the agent's pid file. If the key is provided it's
        added to the agent name as a suffix. If key is not used the default
        pid file path can be set by the **{0}** constant in the Agent class.

        If the pid file is created by the service, the agent can still work
        with this file if the path is defined as the constant.

        :param key: Custom pid file suffix
        :type key: str or None
        :return: Pid file path
        :rtype: str
        """
        if key is not None:
            return os.path.join(self.directory, self.file_name(key))
        return getattr(
            self.agent,
            constants.CONST_PID_FILE,
            os.path.join(self.directory, self.file_name()),
        )

    @property
    def path(self):
        """
        Alias for 'file_path' with the default key

        :return: Pid file path
        :rtype: str
        """
        return self.file_path()

    def make_directory(self):
        """
        Create the pid file directory if it's not present.
        """
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

    def file_is_present(self, key=None):
        """
        Check if the specified pid file is present or not.

        :param key: Custom pid file suffix
        :type key: str or None
        :return: Boolean value
        :rtype: bool
        """
        return os.path.isfile(self.file_path(key))

    @property
    def is_present(self):
        """
        Alias for 'file_is_present' for the default pid file

        :return: Boolean value
        :rtype: bool
        """
        return self.file_is_present()

    present = is_present

    def create_file(self, number, key=None):
        """
        Create the specified pid file and
        write the pid number to it.

        :param number: Pid file number
        :type number: int
        :param key: Custom pid file suffix
        :type key: str or None
        """
        self.make_directory()
        with open(self.file_path(key), 'w') as pid_file:
            pid_file.write("%d\n" % number)

    def create(self, number):
        """
        Alias for 'create_file' for the default pid file.

        :param number: Pid number
        :param number: int
        """
        self.create_file(number)

    def read_file(self, key=None):
        """
        Read the pid file and return the recorded number or
        None if the file cannot be read.

        :param key: Custom pid file suffix
        :type key: str or None
        :return: The pid number
        :rtype: int or None
        """
        if not self.file_is_present(key):
            return None
        with open(self.file_path(key), 'r') as pid_file:
            number = pid_file.read()
        return string_to_integer(number)

    @property
    def read(self):
        """
        Alias for 'read_file' for the default pid file.
        """
        return self.read_file()

    number = read

    def remove_file(self, key=None):
        """
        Remove the specified pid file

        :param key: Custom pid file suffix
        :type key: str or None
        """
        if self.file_is_present(key):
            os.remove(self.file_path(key))

    def remove(self):
        """
        Alias for 'remove_file' for the default pid file.
        """
        self.remove_file()

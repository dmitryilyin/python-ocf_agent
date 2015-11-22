# -*- coding: utf-8 -*-

import os
from ocf_agent import constants
from ocf_agent.helpers import docstring_format


class Lock(object):
    """
    The Lock object can create, check and remove lock files.
    """

    def __init__(self, agent):
        """
        The Lock object should have the Agent object as the first argument.

        :param agent: The parent Agent
        :type agent: Agent
        """
        self.agent = agent

    @property
    @docstring_format(constants.CONST_LOCK_DIR, constants.DEFAULT_LOCK_DIR)
    def directory(self):
        """
        The directory where all the lock files will be placed.
        Can be set by the *{0}* constant in the Agent class
        and will default to **{1}**.

        :return: Lock directory path
        :rtype: str
        """
        return getattr(
            self.agent,
            constants.CONST_LOCK_DIR,
            constants.DEFAULT_LOCK_DIR,
        )

    def file_name(self, key=None):
        """
        The lock file name for this agent with the custom key if the key is
        provided.

        :param key: Custom lock file suffix
        :type key: str or None
        :return: Lock file name
        :rtype: str
        """
        file_name = self.agent.name
        if self.agent.environment.res_instance is not None:
            file_name += '-' + self.agent.environment.res_instance
        if key is not None:
            file_name += '-' + key
        return file_name + '.lock'

    @docstring_format(constants.CONST_LOCK_FILE)
    def file_path(self, key=None):
        """
        The full path to the agent's lock file. If the key is provided it's
        added to the agent name as a suffix. If key is not used the default
        lock file path can be set by the **{0}** constant in the Agent class.

        :param key: Custom lock file suffix
        :type key: str or None
        :return: Lock file path
        :rtype: str
        """
        if key is not None:
            return os.path.join(self.directory, self.file_name(key))
        return getattr(
            self.agent,
            constants.CONST_LOCK_FILE,
            os.path.join(self.directory, self.file_name()),
        )

    @property
    def path(self):
        """
        Alias for 'file_path' with the default key.

        :return: Lock file path
        :rtype: str
        """
        return self.file_path()

    def make_directory(self):
        """
        Create the lock file directory if it's not present.
        """
        if not os.path.isdir(self.directory):
            os.mkdir(self.directory)

    def file_is_present(self, key=None):
        """
        Check if the specified lock file is present or not.

        :param key: Custom lock file suffix
        :type key: str or None
        :return: Boolean value
        :rtype: bool
        """
        return os.path.isfile(self.file_path(key))

    @property
    def is_present(self):
        """
        Alias for 'file_is_present' for the default lock file

        :return: Boolean value
        :rtype: bool
        """
        return self.file_is_present()

    present = is_present

    def create_file(self, key=None):
        """
        Create the specified lock file

        :param key: Custom lock file suffix
        :type key: str or None
        """
        self.make_directory()
        open(self.file_path(key), 'w').close()

    def create(self):
        """
        Alias for 'create_file' for the default lock file.
        """
        self.create_file()

    def remove_file(self, key=None):
        """
        Remove the specified lock file

        :param key: Custom lock file suffix
        :type key: str or None
        """
        if self.file_is_present(key):
            os.remove(self.file_path(key))

    def remove(self):
        """
        Alias for 'remove_file' for the default lock file.
        """
        self.remove_file()

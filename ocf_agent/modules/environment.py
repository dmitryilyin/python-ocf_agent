# -*- coding: utf-8 -*-

import os
from ocf_agent import constants
from ocf_agent.helpers import memoization
from ocf_agent.helpers import string_to_bool
from ocf_agent.helpers import string_to_integer


class Environment(object):
    def __init__(self, agent):
        self.agent = agent

    @property
    @memoization
    def environment(self):
        """
        Returns the dictionary of all relevant environment variables and
        their values
        @rtype: dict
        @return: Dictionary of environment variables and their values
        """
        environment = {}
        for variable in os.environ.keys():
            if variable.startswith('HA_') or \
                    variable.startswith('OCF_') or \
                    variable.startswith('PCMK_'):
                environment[variable] = os.environ[variable]
        return environment

    all = environment

    get = os.getenv

    @property
    @memoization
    def meta(self):
        meta = {}
        for variable in os.environ.keys():
            if variable.startswith(constants.VAR_CRM_META_PREFIX):
                meta_variable_name = \
                    variable[len(constants.VAR_CRM_META_PREFIX):]
                meta[meta_variable_name] = \
                    os.environ[variable]
        return meta

    @property
    @memoization
    def notify(self):
        notify = {}
        for variable in os.environ.keys():
            if variable.startswith(constants.VAR_CRM_NOTIFY_PREFIX):
                notify_variable_name = \
                    variable[len(constants.VAR_CRM_NOTIFY_PREFIX):]
                notify[notify_variable_name] = \
                    os.environ[variable]
        return notify

    @property
    def res_class(self):
        return 'ocf'

    @property
    def res_type(self):
        return os.getenv(
            constants.OCF_VAR_RESOURCE_TYPE,
            None
        )

    @property
    def res_provider(self):
        return os.getenv(
            constants.OCF_VAR_RESOURCE_PROVIDER,
            None
        )

    @property
    def res_instance(self):
        return os.getenv(
            constants.OCF_VAR_RESOURCE_INSTANCE,
            self.agent.name,
        )

    @property
    def instance_name(self):
        if self.res_instance is None:
            return None
        instance = self.res_instance.split(':')
        return instance[0]

    instance = instance_name

    @property
    def instance_suffix(self):
        if self.res_instance is None:
            return None
        instance = self.res_instance.split(':')
        if len(instance) < 2:
            return None
        return instance[1]

    @property
    @memoization
    def check_level(self):
        return string_to_integer(
            os.getenv(
                constants.OCF_VAR_CHECK_LEVEL,
                constants.DEFAULT_DEPTH,
            )
        )

    depth = check_level

    @property
    @memoization
    def ra_version_major(self):
        return string_to_integer(
            os.getenv(
                constants.OCF_VAR_RA_VERSION_MAJOR,
                1,
            )
        )

    @property
    @memoization
    def ra_version_minor(self):
        return string_to_integer(
            os.getenv(
                constants.OCF_VAR_RA_VERSION_MINOR,
                0,
            )
        )

    @property
    @memoization
    def is_debug(self):
        return string_to_bool(
            os.getenv(
                constants.OCF_VAR_DEBUG,
                False,
            ),
            False,
        )

    @property
    @memoization
    def is_logd(self):
        return string_to_bool(
            os.getenv(
                constants.OCF_VAR_LOGD,
                False,
            ),
            False,
        )

    @property
    def log_facility(self):
        return os.getenv(
            constants.OCF_VAR_LOG_FACILITY,
            constants.DEFAULT_LOG_FACILITY,
        )

    @property
    def ocf_root(self):
        return os.getenv(
            constants.OCF_VAR_ROOT,
            constants.DEFAULT_OCF_ROOT,
        )

    @property
    def cluster_type(self):
        return os.getenv(
            constants.OCF_VAR_CLUSTER_TYPE,
            constants.DEFAULT_CLUSTER_TYPE,
        )

    @property
    def quorum_type(self):
        return os.getenv(
            constants.OCF_VAR_QUORUM_TYPE,
            constants.DEFAULT_QUORUM_TYPE,
        )

    @property
    @memoization
    def meta_master_max(self):
        return string_to_integer(
            os.getenv(
                constants.OCF_VAR_META_MASTER_MAX,
                None
            )
        )

    @property
    @memoization
    def meta_clone_max(self):
        return string_to_integer(
            os.getenv(
                constants.OCF_VAR_META_CLONE_MAX,
                None
            )
        )

    @property
    @memoization
    def meta_master(self):
        return string_to_integer(
            os.getenv(
                constants.OCF_VAR_META_MASTER,
                None
            )
        )

    @property
    @memoization
    def meta_clone(self):
        return string_to_integer(
            os.getenv(
                constants.OCF_VAR_META_CLONE,
                None
            )
        )

    @property
    @memoization
    def is_clone(self):
        return self.meta_clone_max is not None and self.meta_clone_max > 0

    @property
    @memoization
    def is_ms(self):
        return self.meta_master_max is not None and self.meta_master_max > 0

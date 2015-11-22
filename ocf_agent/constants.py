# -*- coding: utf-8 -*-

"""
:var OCF_SUCCESS: The exit code of successful action.
    For monitor action it's the exit code of the running agent or
    successful test.
    For multi-state monitor it's the exit code of the agent running
    in the Slave mode.
"""

OCF_SUCCESS = 0
OCF_ERR_GENERIC = 1
OCF_ERR_ARGS = 2
OCF_ERR_UNIMPLEMENTED = 3
OCF_ERR_PERM = 4
OCF_ERR_INSTALLED = 5
OCF_ERR_CONFIGURED = 6
OCF_NOT_RUNNING = 7
OCF_RUNNING_MASTER = 8
OCF_FAILED_MASTER = 9

ENV_MANDATORY = [
    "OCF_ROOT",
    "OCF_RA_VERSION_MAJOR",
    "OCF_RA_VERSION_MINOR",
    "OCF_RESOURCE_INSTANCE",
    "OCF_RESOURCE_TYPE",
]

HANDLERS_MANDATORY = [
    "start",
    "stop",
    "monitor",
]

HANDLERS_OPTIONAL = [
    "promote",
    "demote",
    "migrate_to",
    "migrate_from",
    "notify",
    "recover",
    "reload",
]

BUILTIN_HANDLERS = [
    "usage",
    "meta-data",
    "validate-all",
]

ALIAS_HANDLERS = {
    'status': 'monitor',
    'help': 'usage',
    'restart': 'reload',
    'validate': 'validate-all',
    'meta': 'meta-data',
}

VALID_HANDLERS = HANDLERS_MANDATORY + HANDLERS_OPTIONAL

VAR_PARAMETER_PREFIX = 'OCF_RESKEY_'
VAR_CRM_META_PREFIX = 'OCF_RESKEY_CRM_meta_'
VAR_CRM_NOTIFY_PREFIX = 'OCF_RESKEY_CRM_meta_notify_'
PARAMETER_CLASS_PREFIX = 'OCFParameter_'
HANDLER_CLASS_PREFIX = 'OCFHandler_'
OCF_HANDLER_METHOD_PREFIX = 'handler_'
CONST_MEMOIZATION = '__memoization__'

DEFAULT_LANGUAGE = 'en'
DEFAULT_ENCODING = 'utf-8'
DEFAULT_VERSION = '1'
DEFAULT_INTERVAL = '10'
DEFAULT_TIMEOUT = '20'
DEFAULT_DEPTH = '0'
DEFAULT_LOG_FACILITY = 'daemon'
DEFAULT_OCF_ROOT = '/usr/lib/ocf'
DEFAULT_CLUSTER_TYPE = 'corosync'
DEFAULT_QUORUM_TYPE = 'pcmk'

OCF_VAR_RESOURCE_TYPE = 'OCF_RESOURCE_TYPE'
OCF_VAR_RESOURCE_PROVIDER = 'OCF_RESOURCE_PROVIDER'
OCF_VAR_RESOURCE_INSTANCE = 'OCF_RESOURCE_INSTANCE'
OCF_VAR_CHECK_LEVEL = 'OCF_CHECK_LEVEL'
OCF_VAR_RA_VERSION_MINOR = 'OCF_RA_VERSION_MINOR'
OCF_VAR_RA_VERSION_MAJOR = 'OCF_RA_VERSION_MAJOR'
OCF_VAR_DEBUG = 'HA_debug'
OCF_VAR_LOGD = 'HA_LOGD'
OCF_VAR_LOG_FACILITY = 'HA_LOGFACILITY'
OCF_VAR_ROOT = 'OCF_ROOT'
OCF_VAR_CLUSTER_TYPE = 'HA_cluster_type'
OCF_VAR_QUORUM_TYPE = 'HA_quorum_type'
OCF_VAR_META_MASTER_MAX = 'OCF_RESKEY_CRM_meta_master_max'
OCF_VAR_META_CLONE_MAX = 'OCF_RESKEY_CRM_meta_clone_max'
OCF_VAR_META_MASTER = 'OCF_RESKEY_CRM_meta_master'
OCF_VAR_META_CLONE = 'OCF_RESKEY_CRM_meta_clone'
OCF_VAR_META_MIGRATE_SOURCE = 'OCF_RESKEY_CRM_meta_migrate_source'
OCF_VAR_META_MIGRATE_TARGET = 'OCF_RESKEY_CRM_meta_migrate_target'

VALID_ROLES = [
    'Master',
    'Slave',
]

CONST_ACTION = 'ACTION'
CONST_NAME = 'NAME'
CONST_SHORT_DESCRIPTION = 'SHORTDESC'
CONST_LONG_DESCRIPTION = 'LONGDESC'
CONST_LANGUAGE = 'LANG'
CONST_DEFAULT = 'DEFAULT'
CONST_REQUIRED = 'REQUIRED'
CONST_UNIQUE = 'UNIQUE'
CONST_VERSION = 'VERSION'
CONST_ENCODING = 'ENCODING'
CONST_TIMEOUT = 'TIMEOUT'
CONST_INTERVAL = 'INTERVAL'
CONST_DEPTH = 'DEPTH'
CONST_ROLE = 'ROLE'
CONST_METHOD = 'METHOD'

VALUES_TRUE = frozenset(("1", "t", "true", "yes", "y", 'on'))
VALUES_FALSE = frozenset(("0", "f", "false", "no", "n", 'off'))

# lock module
DEFAULT_LOCK_DIR = '/var/lock/pacemaker'
CONST_LOCK_DIR = 'LOCK_DIR'
CONST_LOCK_FILE = 'LOCK_FILE'

# pid module
DEFAULT_PID_DIR = '/var/run/pacemaker'
CONST_PID_DIR = 'PID_DIR'
CONST_PID_FILE = 'PID_FILE'

# log module
HA_LOGD_SOCKET = '/var/lib/heartbeat/log_daemon'
SYSLOG_SOCKET = '/dev/log'
LOG_FILE_DIRECTORY = '/var/log/corosync'
DEFAULT_LOG_HANDLERS = ['console', 'syslog']
CONST_HANDLERS = 'LOG_HANDLERS'

# process module
KILL_SIGNAL_RETRY = 5
TERM_SIGNAL_RETRY = 5

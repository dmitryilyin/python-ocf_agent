import sys
from ocf_agent import constants
from ocf_agent.helpers import docstring_format


class Exit(object):
    """
    The exit object handlers the Agent's exit conditions, exit codes
    and logging.
    """

    def __init__(self, agent):
        """
        The Exit object should be created with the Agent parent object as
        the first argument.

        :param agent: Parent Agent
        :type agent: Agent
        """
        self.agent = agent

    def output(self, event, message, code):
        """
        Output the exit message to the Agent's logger

        :param event: Exit event name
        :type event: str
        :param message: Exit event message
        :type message: str
        :param code: Exit code
        :type code: int
        """
        self.agent.log.info(
            '%s: %s - exit code: %d' % (event, message, code)
        )

    @docstring_format(constants.OCF_SUCCESS)
    def success(self, message):
        """
        There was no error and the action have completed successfully.
        It is the expected result of any action like start, stop, promote,
        and demote. The agent will exit with code **{0}**.

        For the monitor action of a simple or cloned service this exit code
        means that the service is running and all checks have passed.

        For the multi-state service this exit code means that the service is
        running in the Slave mode.
        If the service is running in the Master mode is should return return
        OCFRunningMaster instead.

        :param message: Event message
        :type message: str
        """
        self.output(
            'success',
            message,
            constants.OCF_SUCCESS,
        )
        sys.exit(constants.OCF_SUCCESS)

    running = success
    running_slave = success

    @docstring_format(constants.OCF_ERR_GENERIC)
    def error_generic(self, message):
        """
        Generic or unspecified error. This return code **{0}** should be used
        if other error codes cannot describe the problem. The monitor action
        should return this for a crashed, hang, or otherwise failed service.

        The cluster manager will try to recover from this error by restarting
        the agent service on the same node unless configured not to.

        :param message: Event message
        :type message: str
        """
        self.output(
            'success',
            message,
            constants.OCF_ERR_GENERIC,
        )
        sys.exit(constants.OCF_ERR_GENERIC)

    @docstring_format(constants.OCF_ERR_ARGS)
    def error_arguments(self, message):
        """
        Arguments error should be raise if the agent have been called
        without an action or validation have failed. Any action can return
        the code **{0}** in similar cases.

        :param message: Event message
        :type message: str
        """
        self.output(
            'error_arguments',
            message,
            constants.OCF_ERR_ARGS,
        )
        sys.exit(constants.OCF_ERR_ARGS)

    @docstring_format(constants.OCF_ERR_UNIMPLEMENTED)
    def error_unimplemented(self, message):
        """
        The agent have been executed with an action that is not implemented
        or the handler method is missing. For example, if an agent does not
        support multi-state configuration but is asked to do promote or demote
        it should return exit code **{0}**.

        :param message: Event message
        :type message: str
        """
        self.output(
            'error_unimplemented',
            message,
            constants.OCF_ERR_UNIMPLEMENTED,
        )
        sys.exit(constants.OCF_ERR_UNIMPLEMENTED)

    @docstring_format(constants.OCF_ERR_PERM)
    def error_permissions(self, message):
        """
        THe agent was not able to perform an action due to a permission
        problem. It could not open a file, socket or write to a directory.
        The return code should be **{0}**.

        The cluster manager will try to start the failed resource on the
        other node because this error is counted as an unrecoverable.

        :param message: Event message
        :type message: str
        """
        self.output(
            'error_permissions',
            message,
            constants.OCF_ERR_PERM,
        )
        sys.exit(constants.OCF_ERR_PERM)

    @docstring_format(constants.OCF_ERR_INSTALLED)
    def error_installation(self, message):
        """
        The executable binary is not installed or the resource is
        misconfigured and cannot find its binary. The return code should
        be **{0}**.

        This error is treated as fatal and the cluster will not try to recover
        the resource neither on the same node nor on any other until the
        problem is fixed and resource is is cleaned up.

        :param message: Event message
        :type message: str
        """
        self.output(
            'error_installation',
            message,
            constants.OCF_ERR_INSTALLED,
        )
        sys.exit(constants.OCF_ERR_INSTALLED)

    @docstring_format(constants.OCF_ERR_CONFIGURED)
    def error_configuration(self, message):
        """
        The resource is misconfigured by a user. For example, parameter have
        been given an incorrect value type. The return code should
        be **{0}**.

        This error is treated as fatal and the cluster will not try to
        restart the resource and will wait for a user intervention.

        :param message: Event message
        :type message: str
        """
        self.output(
            'error_configuration',
            message,
            constants.OCF_ERR_CONFIGURED,
        )
        sys.exit(constants.OCF_ERR_CONFIGURED)

    @docstring_format(constants.OCF_NOT_RUNNING)
    def not_running(self, message):
        """
        The exit code **{0}** should be returned only by a monitor action if
        the service is not running. It should be *cleanly* stopped service,
        not a crashed one.

        If the service is not running due to some error, other exit codes
        should be used and the stop action should return 'success' code if
        completed successfully.

        :param message: Event message
        :type message: str
        """
        self.output(
            'not_running',
            message,
            constants.OCF_NOT_RUNNING,
        )
        sys.exit(constants.OCF_NOT_RUNNING)

    @docstring_format(constants.OCF_RUNNING_MASTER)
    def running_master(self, message):
        """
        The exit code **{0}** should only be returned by a monitor action in
        the master-slave configuration when it have determined that the
        resource is currently running in the Master mode. IF the resource
        is running in the Slave mode it should return the 'success' exit code.

        :param message: Event message
        :type message: str
        """
        self.output(
            'running_master',
            message,
            constants.OCF_RUNNING_MASTER,
        )
        sys.exit(constants.OCF_RUNNING_MASTER)

    @docstring_format(constants.OCF_FAILED_MASTER)
    def master_failed(self, message):
        """
        In the multi-state configuration exit code **{0}** should be returned
        by a monitor action if the resource have failed in the master mode.

        The cluster will try to recover the resource in-place by stopping,
        starting and promoting it again.

        :param message: Event message
        :type message: str
        """
        self.output(
            'master_failed',
            message,
            constants.OCF_FAILED_MASTER,
        )
        sys.exit(constants.OCF_FAILED_MASTER)

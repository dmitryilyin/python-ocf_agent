import psutil
from ocf_agent.helpers import string_to_integer
from subprocess import PIPE
from time import sleep
from ocf_agent import constants


class Process(object):
    def __init__(self, agent):
        self.agent = agent

    @property
    def iterator(self):
        return psutil.process_iter()

    @property
    def processes(self):
        return list(self.iterator)

    all = processes

    def find(self, name):
        return [
            process for process in self.iterator
            if name in process.name or name in ' '.join(process.cmdline)
            ]

    @staticmethod
    def is_running(pid):
        pid = string_to_integer(pid)
        return psutil.pid_exists(pid)

    @staticmethod
    def get(pid):
        pid = string_to_integer(pid)
        try:
            return psutil.Process(pid)
        except (TypeError, psutil.NoSuchProcess):
            return None

    def kill(self, pid):
        process = self.get(pid)
        if process is not None:
            process.kill()

    def terminate(self, pid):
        process = self.get(pid)
        if process is None:
            return
        process.terminate()

    def ensure_terminate(self, pid):
        process = self.get(pid)
        if process is None:
            return True
        for i in range(constants.TERM_SIGNAL_RETRY):
            if not process.is_running():
                return True
            try:
                process.terminate()
            except psutil.NoSuchProcess:
                return True
            sleep(1)
        return self.ensure_kill(pid)

    def ensure_kill(self, pid):
        process = self.get(pid)
        if process is None:
            return True
        for i in range(constants.KILL_SIGNAL_RETRY):
            if not process.is_running():
                return True
            try:
                process.kill()
            except psutil.NoSuchProcess:
                return True
            sleep(1)
        return False

    @staticmethod
    def sub(*args, **kwargs):
        process = psutil.Popen(args, stdout=PIPE, stderr=PIPE, **kwargs)
        stdout, stderr = process.communicate()
        process.wait()
        return {
            'stdout': stdout,
            'stderr': stderr,
            'code': process.returncode,
            'process': process,
        }

    @staticmethod
    def run(*args, **kwargs):
        process = psutil.Popen(args, **kwargs)
        process.communicate()
        process.wait()
        return process.returncode

    def run_shell(self, command, **kwargs):
        return self.run(command, shell=True, **kwargs)

    def sub_shell(self, command, **kwargs):
        return self.sub(command, shell=True, **kwargs)

    @staticmethod
    def daemonize(*args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        # TODO: need to fork twice to prevent children from becoming zombies
        process = psutil.Popen(
            args,
            shell=False,
            stdin=None,
            stdout=None,
            stderr=None,
            close_fds=True,
            cwd='/',
            **kwargs
        )
        return process

# TODO: a method to kill a process and all of its children

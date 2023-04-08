"""
Ansible exceptions
"""
from ansible_runner import Runner
from typing import Optional


class KnownAnsibleError(Exception):
    """
    Base exception for errors by Ansible and ansible-runner
    """

    def __init__(self, runner: Runner, err_msg: str, error_output: Optional[str] = None):
        super().__init__()
        self.runner_rc = runner.rc,
        self.runner_status = runner.status,
        self.runner_stats = runner.stats,
        self.info = "Ansible error [rc: {rc}] (status {status}. \n" \
                    "Ansible stats: {stats} \n".format(rc=self.runner_rc,
                                                       status=self.runner_status,
                                                       stats=self.runner_stats)
        self.err_message = err_msg,
        self.error_output = error_output

    def __str__(self):
        return "{}\n{}".format(self.err_message, self.info)


class AnsibleNoHostsMatched(KnownAnsibleError):
    """
    Class of the exception that may be raised in the course of executing ansible task when there were no processed hosts
    """

    def __init__(self, runner: Runner, host_pattern: str):
        super().__init__(runner,
                         err_msg="No hosts matched! There're no any processed host "
                                 "(host pattern: '{pattern}'). \n".format(pattern=host_pattern))


class AnsibleExecuteError(KnownAnsibleError):
    """
    Class of the exception that may be raised in the course of executing ansible tasks
    """

    def __init__(self, runner: Runner, host_pattern: str, ansible_entity_name: str, fatal_output: Optional[str]):
        super().__init__(runner,
                         err_msg="Ansible execution error of '{entity_name}' "
                                 "(host pattern: '{pattern}'). \n".format(entity_name=ansible_entity_name,
                                                                          pattern=host_pattern),
                         error_output=fatal_output if fatal_output else runner.stdout.read())

"""
Ansible exceptions
"""
from typing import Optional

from ansible_runner import Runner


class KnownAnsibleError(Exception):
    """
    Base exception for errors by Ansible and ansible-runner
    """

    def __init__(self, runner: Runner, err_msg: str, error_output: Optional[str] = None):
        super().__init__()
        self.runner_rc = runner.rc
        self.runner_status = runner.status
        self.runner_stats = runner.stats
        self.info = f"Ansible error [rc: {self.runner_rc}] (status {self.runner_status}. \n" \
                    f"Ansible stats: {self.runner_stats} \n"
        self.err_message = err_msg
        self.error_output = error_output

    def __str__(self):
        return f"{self.err_message}\n{self.info}"


class AnsibleNoHostsMatched(KnownAnsibleError):
    """
    Class of the exception that may be raised in the course of executing ansible task when there were no processed hosts
    """

    def __init__(self, runner: Runner, host_pattern: str):
        super().__init__(runner,
                         err_msg="No hosts matched! There are no any processed host "
                                 f"(host pattern: '{host_pattern}'). \n")


class AnsibleExecuteError(KnownAnsibleError):
    """
    Class of the exception that may be raised in the course of executing ansible jobs
    """

    def __init__(self, runner: Runner, host_pattern: str, ansible_entity_name: str, fatal_output: Optional[str]):
        super().__init__(runner,
                         err_msg=f"Ansible execution error of '{ansible_entity_name}' "
                                 f"(host pattern: '{host_pattern}'). \n",
                         error_output=fatal_output if fatal_output else runner.stdout.read())


class IgnoredAnsibleFailure(KnownAnsibleError):
    """
    Class of the exception that may be raised when errors where ignored during execution
    """

    def __init__(self, runner: Runner, err_msg: str):
        super().__init__(runner, err_msg=err_msg)

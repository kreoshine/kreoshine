"""
Package is responsible for executing ansible tasks via ansible-runner
"""
from ansible.executors import AnsibleModuleExecutor, AnsiblePlaybookExecutor


class AnsibleExecutor:
    """
    Contains an asynchronous API for Ansible:
        - ad-hoc command executor
        - playbook executor
    """

    def __init__(self, host_pattern: str, private_data_dir: str, verbosity: int):
        self._host_pattern = host_pattern
        self._module_executor = AnsibleModuleExecutor(host_pattern, private_data_dir, verbosity)
        self._playbook_executor = AnsiblePlaybookExecutor(host_pattern, private_data_dir, verbosity)

    @property
    def target_host_pattern(self) -> str:
        """ Target host pattern for which ansible executor is running """
        return self._host_pattern

    @property
    def ansible_module(self) -> AnsibleModuleExecutor:
        """ Executes ad-hoc command """
        return self._module_executor

    @property
    def ansible_playbook(self) -> AnsiblePlaybookExecutor:
        """ Executes ansible playbooks """
        return self._playbook_executor

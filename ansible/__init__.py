"""
Package is responsible for executing ansible tasks via ansible-runner
"""
import os

from ansible.executors import AnsibleModuleExecutor, AnsiblePlaybookExecutor
from ansible.executors.role_executor import AnsibleRoleExecutor


class AnsibleExecutor:
    """
    Contains an asynchronous API for Ansible:
        - ad-hoc command executor
        - playbook executor
    """

    def __init__(self, host_pattern: str, private_data_dir: str, verbosity: int):
        self._private_data_dir = private_data_dir
        self._host_pattern = host_pattern
        self._module_executor = AnsibleModuleExecutor(host_pattern, private_data_dir, verbosity)
        self._playbook_executor = AnsiblePlaybookExecutor(host_pattern, private_data_dir, verbosity)
        self._role_executor = AnsibleRoleExecutor(host_pattern, private_data_dir, verbosity)

    @property
    def runner_inventory_file(self) -> str:
        """ Default inventory file for ansible-runner """
        return os.path.join(self._private_data_dir, 'inventory/hosts')

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

    @property
    def ansible_roles(self) -> AnsibleRoleExecutor:
        """ Executes ansible roles """
        return self._role_executor

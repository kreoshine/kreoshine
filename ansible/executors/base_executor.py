"""
Module contain abstract ansible executor as a base helper class
"""
import logging

from typing import List, Optional

import ansible_runner
from ansible_runner import Runner, AnsibleRunnerException
from ansible.exceptions import AnsibleExecuteError, AnsibleNoHostsMatched

logger = logging.getLogger('ansible_deploy')


class BaseAnsibleExecutor:
    """
    Class contains logic for launching and analysing `runner` in synchronous way
    """
    def __init__(self, host_pattern: str, private_data_dir: str, verbosity: int, ssh_key: str):
        self._host_pattern = host_pattern
        self._private_data_dir = private_data_dir
        self._verbosity = verbosity
        self._ssh_key = ssh_key

    @property
    def host_pattern(self) -> str:
        """ Target host pattern for which ansible executor is running """
        return self._host_pattern

    @property
    def success_rc(self) -> int:
        """ Successful result of ansible task execution """
        return 0

    def _execute_ansible_runner(self, params_to_execute: dict) -> Runner:
        """        (Synchronously!)
        Entry point for ansible-runner execution

        Sets several params (such as verbosity and 'private data dir') before execution

        Args:
            params_to_execute: params for ansible-runner (for more info see `ansible-runner/interface.py`)
        Returns:
            ansible runner object after execution
        """
        # set ansible verbosity level
        params_to_execute['verbosity'] = self._verbosity

        # directory where ansible artifacts will be stored
        params_to_execute['private_data_dir'] = self._private_data_dir

        # params_to_execute['ssh_key'] = self._ssh_key

        runner = ansible_runner.run(**params_to_execute)
        return runner

    def _check_runner_execution(self, runner: Runner, host_pattern: str, executed_entity: str) -> None:
        """
        Checks runner execution

        Args:
            runner: runner object gotten after execution
            host_pattern: hostname pattern that has been using for ansible execution (e.g. hostname)
            executed_entity: entity that was executed (e.g. playbook, module)
        Raises:
            AnsibleNoHostsMatched: when none of the hosts where processed
            AnsibleExecuteError: when error happened during execution
        """
        if runner.rc == 1:
            print('Erorr')
            return
        if not runner.stats['processed']:
            logger.warning('None of the hosts were processed!')
            raise AnsibleNoHostsMatched(runner, host_pattern=host_pattern)

        if runner.rc != self.success_rc:
            logger.error("Unsuccessful ansible result code [rc=%s}]", runner.rc)
            fatal_message = self.__get_fatal_output_message(runner)

            logger.debug("For more info see ansible artifact: %s", runner.config.artifact_dir)
            raise AnsibleExecuteError(runner, host_pattern=host_pattern,
                                      ansible_entity_name=executed_entity, fatal_output=fatal_message)

    def __get_fatal_output_message(self, runner: Runner) -> Optional[str]:
        """
        Gets output lines start with word 'fatal' from runner and forms message

        If several lines are found, it merges them into one using a newline.

        Args:
            runner:  ansible runner received after playbook execution

        Returns:
            fatal output message
        """
        fatal_output = self._find_lines(runner, start_with='fatal')
        if len(fatal_output) == 1:
            return fatal_output[0]
        if len(fatal_output) == 0:
            return None
        # len(fatal_output) > 1:
        return '\r\n'.join(fatal_output)

    @staticmethod
    def _find_lines(runner: Runner, start_with: str = '') -> List[str]:
        """
        Searches in runner stdout the lines that start with specific word

        Args:
            runner: ansible runner received after playbook execution
            start_with: selects lines that start with it
        Returns:
            list of received messages
        """
        output_lines = []
        try:
            for line in runner.stdout.readlines():
                if line.startswith(start_with):
                    output_lines.append(line)
        except AnsibleRunnerException:
            logger.exception("Could not find stdout in runner object")
        return output_lines

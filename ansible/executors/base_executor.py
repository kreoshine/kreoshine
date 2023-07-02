"""
Module contain abstract ansible executor as a base helper class
"""
import logging

from typing import List, Optional

import ansible_runner
from ansible_runner import Runner, AnsibleRunnerException

from ansible import ansible_const
from ansible.exceptions import AnsibleExecuteError, AnsibleNoHostsMatched, IgnoredAnsibleFailure, KnownAnsibleError

logger = logging.getLogger('ansible_deploy')


class BaseAnsibleExecutor:
    """
    Class contains logic for launching and analysing `runner` in synchronous way
    """
    def __init__(self, host_pattern: str, private_data_dir: str, verbosity: int):
        self._host_pattern = host_pattern
        self._private_data_dir = private_data_dir
        self._verbosity = verbosity

    @property
    def host_pattern(self) -> str:
        """ Target host pattern for which ansible executor is running """
        return self._host_pattern

    @property
    def success_rc(self) -> int:
        """ Successful result of ansible task execution """
        return 0

    @property
    def failed_execution_rc(self) -> int:
        """ Result code when usually task failed during a play

        Notes: this result code can also mean:
            - user interrupting;
            - invalid or unexpected arguments, i.e. ansible-playbook --this-arg-doesnt-exist some_playbook.yml
            - parsing error was encountered during a dynamic include
        """
        return 2

    def _execute_ansible_runner(self, params_to_execute: dict, need_to_set_host_pattern: bool = True) -> Runner:
        """        (Synchronously!)
        Entry point for ansible-runner execution

        Sets several params (such as `verbosity` and `private data dir` and so on) before execution

        Args:
            params_to_execute: params for ansible-runner (for more info see `ansible-runner/interface.py`)
            need_to_set_host_pattern: boolean reflecting the need to set the host template, by default True
        Returns:
            ansible runner object after execution
        """
        if need_to_set_host_pattern:
            self._set_target_host_pattern(params_to_execute)

        logger.debug("Collected next params (most important) for ansible runner: %s", params_to_execute)
        # set ansible verbosity level
        params_to_execute['verbosity'] = self._verbosity

        # directory where ansible artifacts will be stored
        params_to_execute['private_data_dir'] = self._private_data_dir

        runner = ansible_runner.run(**params_to_execute)
        return runner

    def _set_target_host_pattern(self, params_to_execute: dict) -> None:
        """ Sets target host pattern in params for runner execution """
        if params_to_execute.get('module'):
            params_to_execute['host_pattern'] = self.host_pattern
            return
        if not params_to_execute.get('extravars'):
            params_to_execute['extravars'] = {}
        params_to_execute['extravars'][ansible_const.HOST_PATTERN] = self.host_pattern

    def _check_runner_execution(self, runner: Runner, executed_entity: str) -> None:
        """
        Checks runner execution

        Args:
            runner: runner object gotten after execution
            executed_entity: entity that was executed (e.g. playbook, module)
        Raises:
            AnsibleNoHostsMatched: when none of the hosts where processed
            AnsibleExecuteError: when error happened during execution
            IgnoredAnsibleFailure: when expected error was occurred during execution;
                e.g. "ignore_errors: True" in a task during playbook execution
        """
        if not runner or not runner.stats.get('processed'):
            logger.warning('None of the hosts were processed!')
            raise AnsibleNoHostsMatched(runner, host_pattern=self.host_pattern)

        if runner.rc == self.success_rc:
            return

        logger.warning("Unsuccessful ansible result code [rc=%s}]", runner.rc)
        fatal_message = self.__get_fatal_output_message(runner)

        if runner.rc == self.failed_execution_rc:
            logger.debug("For more info see ansible artifact: %s", runner.config.artifact_dir)
            raise AnsibleExecuteError(runner, host_pattern=self.host_pattern,
                                      ansible_entity_name=executed_entity, fatal_output=fatal_message)
        if runner.stats['ignored']:
            raise IgnoredAnsibleFailure(runner, err_msg="Expected failure has occurred")
        raise KnownAnsibleError(
            runner,
            err_msg="Unexpected error",
            error_output=fatal_message
        )

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

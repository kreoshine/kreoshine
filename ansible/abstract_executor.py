"""
Module is responsible for runner launching
"""
import logging
import os

from typing import List, Optional

import ansible_runner
from ansible_runner import Runner, AnsibleRunnerException

from ansible import ansible_const
from ansible.exceptions import AnsibleExecuteError, AnsibleNoHostsMatched

logger = logging.getLogger('ansible_deploy')


class AbstractAnsibleExecutor:
    """
    Class contains private methods for launching `runner` in various ways
    """

    def __init__(self, private_data_dir: str, verbosity: int):
        self._private_data_dir = private_data_dir
        self._verbosity = verbosity

    @property
    def success_rc(self) -> int:
        """ Successful result of ansible task execution """
        return 0

    def _run_playbook(self, params_to_execute: dict) -> Runner:
        """
        (Synchronously!)
        Launches ansible runner with passed parameters as an `ansible-playbook` command

        Args:
            params_to_execute: parameters to be used to launch runner

        Returns:
            ansible runner object after execution
        """
        assert 'playbook' in params_to_execute, "Argument 'playbook' must be defined for a playbook execution"
        playbook_name = os.path.basename(params_to_execute['playbook'])
        logger.info("Initiate '%s' playbook to execute", playbook_name)

        logger.debug("Collected next params for ansible runner: %s", params_to_execute)

        # set ansible verbosity level
        params_to_execute['verbosity'] = self._verbosity

        # directory where ansible artifacts will be stored
        params_to_execute['private_data_dir'] = self._private_data_dir

        # entry point of playbook execution
        runner = ansible_runner.run(**params_to_execute)
        logger.info("Stats of '%s' playbook execution: %s", playbook_name, runner.stats)

        self._check_runner_execution(runner,
                                     host_pattern=params_to_execute['extravars'][ansible_const.HOST_PATTERN],
                                     executed_entity=playbook_name)
        return runner

    def _run_ad_hoc_command(self, params_to_execute: dict) -> Runner:
        """
        (Synchronously!)
        Launches ansible runner with passed parameters as an `ad-hoc` command

        Args:
            params_to_execute: parameters to be used to launch runner

        Returns:
            ansible runner object after execution
        """
        assert 'module' in params_to_execute, "Argument 'module' must be defined for an ad-hoc command execution"
        module_name = params_to_execute['module']
        logger.info("Initiate '%s' module to execute", module_name)

        logger.debug("Collected next params for ansible runner: %s", params_to_execute)

        # set ansible verbosity level
        params_to_execute['verbosity'] = self._verbosity

        # directory where ansible artifacts will be stored
        params_to_execute['private_data_dir'] = self._private_data_dir

        # entry point of module execution
        runner = ansible_runner.run(**params_to_execute)
        logger.debug("Stats of '%s' module execution: %s", module_name, runner.stats)

        self._check_runner_execution(runner,
                                     host_pattern=params_to_execute['host_pattern'],
                                     executed_entity=module_name)
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

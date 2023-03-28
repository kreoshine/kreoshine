"""
Contains a class responsible for executing ansible tasks via ansible-runner
"""
import asyncio
import os
from pathlib import Path
from pprint import pprint
from typing import List

import ansible_runner
from ansible_runner import Runner, AnsibleRunnerException

from deploy.ansible import ansible_const
from deploy.ansible.exceptions import AnsibleExecuteError
from deploy.deployment import TEMPORARY_DIR

ANSIBLE_PRIVATE_DATA_DIR = os.path.join(TEMPORARY_DIR, 'ansible/')

PLAYBOOK_LOCATION_DIR = os.path.join(str(Path(__file__).parent), 'playbooks/')
ANSIBLE_VERBOSITY = 1


class AnsibleExecutor:
    """
    Represents async methods for running different playbooks
    """

    def __init__(self, destination_host: str):
        self._loop = asyncio.get_event_loop()
        self._destination_host = destination_host

    @property
    def target_host(self) -> str:
        """ Target host for which ansible executor is running """
        return self._destination_host

    @property
    def echo_playbook(self) -> str:
        """ Location of 'echo' playbook file """
        return os.path.join(PLAYBOOK_LOCATION_DIR, 'echo.yml')

    @property
    def file_line_update_playbook(self) -> str:
        """ Location of the 'file_line_update' playbook file """
        return os.path.join(PLAYBOOK_LOCATION_DIR, 'file_line_update.yml')

    @property
    def file_create_playbook(self) -> str:
        """ Location of the 'file_create' playbook file """
        return os.path.join(PLAYBOOK_LOCATION_DIR, 'file_create.yml')

    @property
    def _success(self) -> int:
        """ Successful result of ansible task execution """
        return 0

    @property
    def _ansible_verbosity(self) -> int:
        """ Every extra count of 'v' will provide more debug output """
        return ANSIBLE_VERBOSITY

    def _run_playbook(self, params_to_execute: dict) -> Runner:
        """
        (Synchronously!)
        Launches ansible runner with passed parameters

        Args:
            params_to_execute: parameters to be used to launch runner

        Returns:
            ansible runner object after execution
        """
        assert 'playbook' in params_to_execute, "Argument 'playbook' must be defined for runner execution"
        playbook_name = os.path.basename(params_to_execute['playbook'])
        print(f"Initiate '{playbook_name}' playbook to execute")

        print("Collected next params for ansible runner:")
        pprint(params_to_execute)

        # set ansible verbosity level
        params_to_execute['verbosity'] = self._ansible_verbosity

        # directory where ansible artifacts will be stored
        params_to_execute['private_data_dir'] = ANSIBLE_PRIVATE_DATA_DIR

        # entry point of playbook execution
        runner = ansible_runner.run(**params_to_execute)
        print(f"Stats of '{playbook_name}' playbook execution: {runner.stats}")
        return runner

    async def execute_echo_task(self) -> None:
        """
        Executes ansible ping task

        Note: this is not an ICMP ping

        Raises:
            AnsibleExecuteError: if there was mistake during communication to the target host
        """
        print("\n[echo] task start")

        params_to_execute = {
            'playbook': self.echo_playbook,
            'extravars': {
                ansible_const.HOST_NAME: self.target_host
            }
        }
        runner = await self._loop.run_in_executor(None, self._run_playbook, params_to_execute)

        if runner.rc != self._success:
            print(f"Unsuccessful ansible result code [rc={runner.rc}]")
            fatal_message = self._get_fatal_output_message(runner)
            raise AnsibleExecuteError(err_code=runner.rc,
                                      playbook_file=self.echo_playbook,
                                      fatal_output=fatal_message)

    def _get_fatal_output_message(self, runner: Runner) -> str:
        """
        Gets output lines start with word 'fatal' from runner and forms message

        If several lines are found, it merges them into one using a newline.
        If they not found at all, a special help message is returned.

        Args:
            runner:  ansible runner received after playbook execution
        Returns:
            fatal output message
        """
        fatal_output = self._find_error_lines(runner, start_with='fatal')
        if len(fatal_output) == 1:
            return fatal_output[0]
        if len(fatal_output) == 0:
            return f"Unable to find line starts with 'fatal' word.\n" \
                   f"For more info see ansible artifact: {runner.config.artifact_dir}"
        # len(fatal_output) > 1:
        return '\r\n'.join(fatal_output)

    @staticmethod
    def _find_error_lines(runner: Runner, start_with: str = '') -> List[str]:
        """
        Searches in runner stdout the lines that start with specific word and logs searched lines in ERROR level

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
        except AnsibleRunnerException as err:
            print(f"[{err}] — Could not find stdout in runner object")
        return output_lines

    async def execute_file_line_update_task(self, file_path: str,
                                            string_to_replace: str, new_string: str) -> None:
        """
        Updates line in the file

        Args:
            file_path: path of the target file
            string_to_replace: string to be replaced
            new_string: string to be inserted
        """
        print("\n[file_line_update] task start")

        params_to_execute = {
            'playbook': self.file_line_update_playbook,
            'extravars': {
                ansible_const.HOST_NAME: self.target_host,
                ansible_const.FILE_PATH: str(file_path),
                ansible_const.STRING_TO_REPLACE: string_to_replace,
                ansible_const.NEW_STRING: new_string
            }
        }
        runner = await self._loop.run_in_executor(None, self._run_playbook, params_to_execute)

        if runner.rc != self._success:
            print(f"Unsuccessful ansible result code [rc={runner.rc}]")
            fatal_message = self._get_fatal_output_message(runner)
            raise AnsibleExecuteError(err_code=runner.rc,
                                      playbook_file=self.file_line_update_playbook,
                                      fatal_output=fatal_message)

    async def execute_file_create_task(self, target_dir: str, file_name: str, file_content: str) -> None:
        """
        Creates new file with content in the target directory

        Args:
            target_dir: target directory absolute path
            file_name: basename of creating file
            file_content: content to be added for file
        """
        print("\n[file_create] task start")

        params_to_execute = {
            'playbook': self.file_create_playbook,
            'extravars': {
                ansible_const.HOST_NAME: self.target_host,
                ansible_const.TARGET_DIR: str(target_dir),
                ansible_const.FILE_NAME: str(file_name),
                ansible_const.FILE_CONTENT: file_content
            }
        }
        runner = await self._loop.run_in_executor(None, self._run_playbook, params_to_execute)

        if runner.rc != self._success:
            print(f"Unsuccessful ansible result code [rc={runner.rc}]")
            fatal_message = self._get_fatal_output_message(runner)
            raise AnsibleExecuteError(err_code=runner.rc,
                                      playbook_file=self.file_create_playbook,
                                      fatal_output=fatal_message)


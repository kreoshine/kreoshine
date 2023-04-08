"""
Contains a class responsible for executing ansible tasks via ansible-runner
"""
import asyncio
import logging
import os
from pathlib import Path
from typing import Optional

from ansible import ansible_const
from ansible.abstract_executor import AbstractAnsibleExecutor
from ansible.decorators import error_log_handler

logger = logging.getLogger('ansible_deploy')

PLAYBOOK_LOCATION_DIR = os.path.join(str(Path(__file__).parent), 'playbooks/')


class AnsibleExecutor(AbstractAnsibleExecutor):
    """
    Represents async methods for running different playbooks
    """

    def __init__(self, destination_host: str, private_data_dir: str, verbosity: int):
        super().__init__(private_data_dir, verbosity)
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
    def file_create_playbook(self) -> str:
        """ Location of the 'file_create' playbook file """
        return os.path.join(PLAYBOOK_LOCATION_DIR, 'file_create.yml')

    @error_log_handler
    async def execute_echo_playbook(self, need_gather_facts: bool) -> None:
        """
        Executes echo playbook

        Note: this is not an ICMP ping

        Args:
            need_gather_facts: boolean value reflecting the need to collect facts about the target node
        Raises:
            AnsibleExecuteError: if there was mistake during communication to the target host
        """
        playbook_name = os.path.basename(self.echo_playbook)
        logger.info("\n[%s] playbook", playbook_name)

        params_to_execute = {
            'playbook': self.echo_playbook,
            'extravars': {
                ansible_const.HOST_NAME: self.target_host,
                ansible_const.NEED_GATHER_FACTS: need_gather_facts,
            }
        }
        await self._loop.run_in_executor(None, self._run_playbook, params_to_execute)

    @error_log_handler
    async def execute_file_line_update_task(self, file_path: str,
                                            string_to_replace: str, new_string: str) -> None:
        """
        Updates line in the file

        Args:
            file_path: path of the target file
            string_to_replace: string to be replaced
            new_string: string to be inserted
        """
        module_name = 'ansible.builtin.lineinfile'
        logger.info("\n[%s] task", module_name)

        params_to_execute = {
            'host_pattern': self.target_host,
            'module': module_name,
            'module_args': f"path={str(file_path)}"
                           f"regexp='^{string_to_replace}'"
                           f"line={new_string}"
                           f"firstmatch=true",
        }
        await self._loop.run_in_executor(None, self._run_ad_hoc_command, params_to_execute)

    @error_log_handler
    async def execute_file_create_playbook(self, target_dir: str, file_name: str, file_content: str) -> None:
        """
        Creates new file with content in the target directory

        Args:
            target_dir: target directory absolute path
            file_name: basename of creating file
            file_content: content to be added for file
        """
        playbook_name = os.path.basename(self.file_create_playbook)
        logger.info("\n[%s] task", playbook_name)

        params_to_execute = {
            'playbook': self.file_create_playbook,
            'extravars': {
                ansible_const.HOST_NAME: self.target_host,
                ansible_const.TARGET_DIR: str(target_dir),
                ansible_const.FILE_NAME: str(file_name),
                ansible_const.FILE_CONTENT: file_content
            }
        }
        await self._loop.run_in_executor(None, self._run_playbook, params_to_execute)

    @error_log_handler
    async def execute_user_creation_task(self, user_name: str,
                                         privilege_escalation_group: Optional[str]) -> None:
        """
        Creates new user

        Args:
            user_name: name of the user to create
            privilege_escalation_group: 'sudo' group that will be added for user, optional
        """
        module_name = "ansible.builtin.user"
        logger.info(f"\n[{module_name}] task")

        if privilege_escalation_group:
            module_args = f"name={user_name} " \
                          f"shell='/bin/bash' " \
                          f"groups={privilege_escalation_group} " \
                          f"append=true"
        else:
            module_args = f"name={user_name} " \
                          f"shell='/bin/bash'"

        params_to_execute = {
            'host_pattern': self.target_host,
            'module': module_name,
            'module_args': module_args
        }
        await self._loop.run_in_executor(None, self._run_ad_hoc_command, params_to_execute)

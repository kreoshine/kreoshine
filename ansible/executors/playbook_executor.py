"""
Module is responsible for execution ansible playbooks
"""
import asyncio
import logging
import os
from pathlib import Path

from ansible_runner import Runner

from ansible import ansible_const
from ansible.decorators import error_log_handler
from ansible.executors.base_executor import BaseAnsibleExecutor

logger = logging.getLogger('ansible_deploy')


class PermittedPlaybooksMixin:
    """ Class is responsible for playbook paths resolving """

    @property
    def _playbook_location_dir(self) -> str:
        """ Directory where the playbooks are located """
        return os.path.join(str(Path(__file__).parent.parent.resolve()), 'playbooks/')

    @property
    def echo_playbook(self) -> str:
        """ Path of the 'echo' playbook """
        return os.path.join(self._playbook_location_dir, 'echo.yml')

    @property
    def file_create_playbook(self) -> str:
        """ Path of the 'file_create' playbook """
        return os.path.join(self._playbook_location_dir, 'file_create.yml')


class AnsiblePlaybookExecutor(BaseAnsibleExecutor, PermittedPlaybooksMixin):
    """  Class is responsible for executing playbooks """

    def __init__(self, host_pattern: str, private_data_dir: str, verbosity: int, ssh_key):
        super().__init__(host_pattern=host_pattern,
                         private_data_dir=private_data_dir,
                         verbosity=verbosity,
                         ssh_key=ssh_key)

    def _run_playbook(self, params_to_execute: dict) -> Runner:
        """        (Synchronously!)
        Launches ansible runner with passed parameters as an `ansible-playbook` command

        Args:
            params_to_execute: parameters to be used to launch runner

        Returns:
            ansible runner object after execution
        """
        assert 'playbook' in params_to_execute, "Argument 'playbook' must be defined for a ansible-playbook execution"
        playbook_name = os.path.basename(params_to_execute['playbook'])
        logger.info("Initiate '%s' playbook to execute", playbook_name)

        logger.debug("Collected next params for ansible runner: %s", params_to_execute)
        runner = self._execute_ansible_runner(params_to_execute)

        logger.info("Stats of '%s' playbook execution: %s", playbook_name, runner.stats)
        self._check_runner_execution(runner,
                                     host_pattern=params_to_execute['extravars'][ansible_const.HOST_PATTERN],
                                     executed_entity=playbook_name)
        return runner

    @error_log_handler
    async def echo(self, need_gather_facts: bool) -> None:
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
                ansible_const.HOST_PATTERN: self.host_pattern,
                ansible_const.NEED_GATHER_FACTS: need_gather_facts,
            }
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_playbook, params_to_execute)

    @error_log_handler
    async def create_file(self, target_dir: str, file_name: str, file_content: str) -> None:
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
                ansible_const.HOST_PATTERN: self.host_pattern,
                ansible_const.TARGET_DIR: str(target_dir),
                ansible_const.FILE_NAME: str(file_name),
                ansible_const.FILE_CONTENT: file_content
            }
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_playbook, params_to_execute)

"""
Module with mixin class for execution ansible playbooks
"""
import asyncio
import logging
import os
from abc import ABC

from ansible import ansible_const
from ansible.decorators import error_log_handler
from ansible.mixins.permitted_playbooks import PermittedPlaybooksMixin
from ansible.mixins.support_mixin import BaseExecutorMixin

logger = logging.getLogger('ansible_deploy')


class PlaybookExecutorMixin(BaseExecutorMixin, PermittedPlaybooksMixin, ABC):
    """  Class is responsible for executing playbooks """

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
                ansible_const.HOST_PATTERN: self.target_host_pattern,
                ansible_const.NEED_GATHER_FACTS: need_gather_facts,
            }
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.run_playbook, params_to_execute)

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
                ansible_const.HOST_PATTERN: self.target_host_pattern,
                ansible_const.TARGET_DIR: str(target_dir),
                ansible_const.FILE_NAME: str(file_name),
                ansible_const.FILE_CONTENT: file_content
            }
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.run_playbook, params_to_execute)

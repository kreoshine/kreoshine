"""
Module with mixin class for execution ansible ad-hoc command
"""
import asyncio
import logging
from abc import ABC
from typing import Optional

from ansible.decorators import error_log_handler
from ansible.mixins.support_mixin import BaseExecutorMixin

logger = logging.getLogger('ansible_deploy')


class ModuleExecutorMixin(BaseExecutorMixin, ABC):
    """ Class is responsible for executing ad-hoc commands """

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
            'host_pattern': self.target_host_pattern,
            'module': module_name,
            'module_args': f"path={str(file_path)}"
                           f"regexp='^{string_to_replace}'"
                           f"line={new_string}"
                           f"firstmatch=true",
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_ad_hoc_command, params_to_execute)

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
        logger.info("\n[%s] task", module_name)

        if privilege_escalation_group:
            module_args = f"name={user_name} " \
                          f"shell='/bin/bash' " \
                          f"groups={privilege_escalation_group} " \
                          f"append=true"
        else:
            module_args = f"name={user_name} " \
                          f"shell='/bin/bash'"

        params_to_execute = {
            'host_pattern': self.target_host_pattern,
            'module': module_name,
            'module_args': module_args
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_ad_hoc_command, params_to_execute)

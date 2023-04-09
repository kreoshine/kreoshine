"""
Module with class for execution ansible ad-hoc command
"""
import asyncio
import logging
from typing import Optional

import ansible_runner
from ansible_runner import Runner

from ansible.decorators import error_log_handler
from ansible.executors.abstract_executor import AbstractAnsibleExecutor

logger = logging.getLogger('ansible_deploy')


class AnsibleModuleExecutor(AbstractAnsibleExecutor):
    """ Class is responsible for executing ad-hoc commands """

    def __init__(self, host_pattern: str, private_data_dir: str, verbosity: int):
        super().__init__(host_pattern=host_pattern, private_data_dir=private_data_dir, verbosity=verbosity)

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
        self._add_common_ansible_params(params_to_execute)

        # entry point of module execution
        runner = ansible_runner.run(**params_to_execute)
        logger.debug("Stats of '%s' module execution: %s", module_name, runner.stats)

        self._check_runner_execution(runner,
                                     host_pattern=params_to_execute['host_pattern'],
                                     executed_entity=module_name)
        return runner

    @error_log_handler
    async def update_file_line(self, file_path: str, string_to_replace: str, new_string: str) -> None:
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
            'host_pattern': self.host_pattern,
            'module': module_name,
            'module_args': f"path={str(file_path)}"
                           f"regexp='^{string_to_replace}'"
                           f"line={new_string}"
                           f"firstmatch=true",
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_ad_hoc_command, params_to_execute)

    @error_log_handler
    async def create_user(self, user_name: str, privilege_escalation_group: Optional[str]) -> None:
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
            'host_pattern': self.host_pattern,
            'module': module_name,
            'module_args': module_args
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_ad_hoc_command, params_to_execute)

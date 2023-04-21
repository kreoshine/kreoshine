"""
Module is responsible for execution ansible roles
"""
import asyncio
import logging
import os
from pathlib import Path

from ansible_runner import Runner

from ansible import ansible_const
from ansible.executors.base_executor import BaseAnsibleExecutor
from deploy.deploy_const import PROJECT_ROOT_PATH

logger = logging.getLogger('ansible_deploy')


class AnsibleRoleExecutor(BaseAnsibleExecutor):
    """ Class is responsible for executing roles """

    def __init__(self, host_pattern: str, private_data_dir: str, verbosity: int):
        super().__init__(host_pattern=host_pattern, private_data_dir=private_data_dir, verbosity=verbosity)

    @property
    def _roles_location_dir(self) -> str:
        """ Directory where the roles are located """
        return os.path.join(str(Path(__file__).parent.parent.resolve()), 'roles/')

    @property
    def nginx_role_playbook(self) -> str:
        """ Entry point for nginx role execution """
        return os.path.join(self._roles_location_dir, 'nginx.yml')

    def _run_role(self, params_to_execute: dict) -> Runner:
        """        (Synchronously!)
        Launches ansible runner with passed parameters as an `ad-hoc` command

        Args:
            params_to_execute: parameters to be used to launch runner

        Returns:
            ansible runner object after execution
        """
        assert 'playbook' in params_to_execute, "Argument 'playbook' must be defined as entry point for role execution"
        role_name = os.path.basename(params_to_execute['playbook']).split('.')[0]

        logger.info("Initiate '%s' role to execute", role_name)
        runner = self._execute_ansible_runner(params_to_execute)

        logger.debug("Stats of '%s' role execution: %s", role_name, runner.stats)
        self._check_runner_execution(runner, executed_entity=f'{role_name} role')
        return runner

    async def execute_nginx_role(self):
        """ Executes nginx role:
            - TODO

        """
        params_to_execute = {
            'playbook': self.nginx_role_playbook,
            'extravars': {
                ansible_const.STATIC_ROOT_PATH: str(PROJECT_ROOT_PATH.joinpath('frontend')),
            }
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_role, params_to_execute)

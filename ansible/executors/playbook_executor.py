"""
Module is responsible for execution ansible playbooks
"""
import asyncio
import logging
import os
from pathlib import Path
from typing import List

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
    def docker_installation_playbook(self) -> str:
        """ Path of the 'docker installation' playbook """
        return os.path.join(self._playbook_location_dir, 'docker_installation.yml')

    @property
    def load_docker_images_playbook(self) -> str:
        """ Path of the 'load docker images' playbook """
        return os.path.join(self._playbook_location_dir, 'load_docker_images.yml')

    @property
    def file_create_playbook(self) -> str:
        """ Path of the 'file_create' playbook """
        return os.path.join(self._playbook_location_dir, 'file_create.yml')

class AnsiblePlaybookExecutor(BaseAnsibleExecutor, PermittedPlaybooksMixin):
    """  Class is responsible for executing playbooks """

    def __init__(self, host_pattern: str, private_data_dir: str, verbosity: int):
        super().__init__(host_pattern=host_pattern, private_data_dir=private_data_dir, verbosity=verbosity)

    def _run_playbook(self, params_to_execute: dict) -> Runner:
        """        (Synchronously!)
        Launches ansible runner with passed parameters as an `ansible-playbook` command

        Args:
            params_to_execute: parameters to be used to launch runner

        Returns:
            ansible runner object after execution
        """
        assert 'playbook' in params_to_execute, "Argument 'playbook' must be defined for an ansible-playbook execution"
        playbook_name = os.path.basename(params_to_execute['playbook'])

        logger.info("Initiate '%s' playbook to execute", playbook_name)
        runner = self._execute_ansible_runner(params_to_execute)

        logger.debug("Stats of '%s' playbook execution: %s", playbook_name, runner.stats)
        self._check_runner_execution(runner, executed_entity=f'{playbook_name} playbook')
        return runner

    @error_log_handler
    async def install_docker(self) -> None:
        """ Installs Docker
        Notes: only 'Debian' 'os family' is supported!
        """
        params_to_execute = {
            'playbook': self.docker_installation_playbook,
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_playbook, params_to_execute)

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
        params_to_execute = {
            'playbook': self.echo_playbook,
            'extravars': {
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
        params_to_execute = {
            'playbook': self.file_create_playbook,
            'extravars': {
                ansible_const.TARGET_DIR: str(target_dir),
                ansible_const.FILE_NAME: str(file_name),
                ansible_const.FILE_CONTENT: file_content
            }
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_playbook, params_to_execute)

    async def load_docker_images(self, image_names: List[str]):
        """ Loads docker images
        Args
            images: list of names of images to load
        """
        params_to_execute = {
            'playbook': self.load_docker_images_playbook,
            'extravars': {
                ansible_const.IMAGE_NAMES: image_names,
            }
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_playbook, params_to_execute)

    @error_log_handler
    async def up_nginx_container(
            self,
            local_root_to_static: str,
            local_nginx_deploy_files_dir: str,
            image_name: str,
            container_name: str):
        """ Create custom image for nginx with necessary configuration

        Adds new layers to the image (most important)
            - deleting base nginx config
            - include static files and required configuration file

        Args:
            local_root_to_static: all static files in this directory will be included ias main static files
                note: will overwrite all existing files in target dir of image
                warn: if path will be without '/' symbol it is going to include directory itself at destination dir
            local_nginx_deploy_files_dir: directory with playbook and necessary files for its execution
            image_name: name of the image to create
            container_name: name of the container to up
        """
        # copy docker file to the host and init container with necessary environment
        if not local_root_to_static.endswith('/'):
            local_root_to_static += '/'
        if not local_nginx_deploy_files_dir.endswith('/'):
            local_nginx_deploy_files_dir += '/'

        params_to_execute = {
            'playbook': local_nginx_deploy_files_dir + 'up_nginx_container.yml',
            'extravars': {
                ansible_const.LOCAL_ROOT_TO_STATIC: local_root_to_static,
                ansible_const.NGINX_DEPLOY_FILES_DIR: local_nginx_deploy_files_dir,
                ansible_const.IMAGE_NAME: image_name,
                ansible_const.CONTAINER_NAME: container_name
            }
        }
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._run_playbook, params_to_execute)

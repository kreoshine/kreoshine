"""
Job that make preparation before deployment
"""
import asyncio
import logging
import os

from ansible import AnsibleExecutor
from ansible.exceptions import AnsibleExecuteError, IgnoredAnsibleFailure
from deploy import utils
from deploy.deploy_const import PROJECT_ROOT_PATH, PRODUCTION_MODE, DEVELOPMENT_MODE
from deploy.jobs.connection import echo_host
from settings import config, SETTINGS_ROOT_PATH

logger = logging.getLogger('ansible_deploy')

# pylint: disable = fixme


async def ensure_ansible_communication(ansible: AnsibleExecutor):
    """ Verifies that the ansible-runner inventory file is associated with the ssh key
    If unable to reach host, initiates recreation of inventory file for ansible-runner
    Note: this method should be used only for deployment in development mode!
    """
    private_key: str = str(PROJECT_ROOT_PATH.joinpath(".ssh/id_rsa"))

    async def _create_runner_inventory_file():
        """ Redefines localhost in runner-inventory file with exist and correct ssh-key """
        inventory_file_content = f'{ansible.target_host_pattern} ' \
                                 f'ansible_user=root ' \
                                 f'ansible_ssh_private_key_file={private_key}'
        inventory_creation_task = asyncio.create_task(
            ansible.ansible_playbook.create_file(target_dir=directory_with_inventory_file,
                                                 file_name=os.path.basename(ansible.runner_inventory_file),
                                                 file_content=inventory_file_content))
        await inventory_creation_task

    directory_with_inventory_file = os.path.dirname(ansible.runner_inventory_file)
    try:
        if not os.path.isfile(ansible.runner_inventory_file):
            utils.create_directory(directory_with_inventory_file)
            await _create_runner_inventory_file()
        await echo_host(ansible, need_gather_facts=False)

    except AnsibleExecuteError as err:
        logger.warning("Error during communication with %s", ansible.target_host_pattern)
        if err.runner_rc == 4:  # most likely due to connection problem
            logger.info("Recreating inventory file for ansible-runner (%s)", ansible.runner_inventory_file)
            utils.clear_directory(target_dir=directory_with_inventory_file)
            await _create_runner_inventory_file()
        else:
            raise


async def make_preparation(ansible: AnsibleExecutor):
    """
    Performs pre-deployment jobs regarding the project and in dependency of the deployment mode
    """
    deploy_mode = config.deploy.mode

    if deploy_mode == DEVELOPMENT_MODE:
        # make available absolute project path in deployment
        config.server.project_root_path = PROJECT_ROOT_PATH

        logger.debug("Check connection for Ansible to '%s'", ansible.target_host_pattern)
        await ensure_ansible_communication(ansible)
    # else: no need to define project directory for production — it should be used from configuration

    if deploy_mode == PRODUCTION_MODE:
        # be sure that user admin existing — his home directory will be used for project location
        admin_creation_task = asyncio.create_task(
            ansible.ansible_module.create_user(user_name=config.server.admin.user_name,
                                               privilege_escalation_group=config.server.admin.sudo_group))
        await admin_creation_task
        # todo: clone repository to admin home dir

    logger.debug("Define '%s' environment for dynaconf: %s", deploy_mode, os.path.join(SETTINGS_ROOT_PATH, '.env'))
    dote_env_content = f'export KREOSHINE_ENV={deploy_mode.upper()}'
    env_creation_task = asyncio.create_task(ansible.ansible_playbook.create_file(target_dir=SETTINGS_ROOT_PATH,
                                                                                 file_name='.env',
                                                                                 file_content=dote_env_content))
    await env_creation_task


async def install_docker(ansible: AnsibleExecutor):
    """ Installs Docker if necessary
    Args:
        ansible: instance of ansible executor
    """
    command_to_check_docker = 'docker --version'
    try:
        logger.debug("Check Docker existence")
        docker_existence_task = ansible.ansible_module.execute_command(command=command_to_check_docker)
        await docker_existence_task
        logger.info("Docker already exist — no need for installation")
    except AnsibleExecuteError:
        logger.debug("Unable to execute command '%s' — trying to install it", command_to_check_docker)
        try:
            logger.debug("Installation docker on %s host", ansible.target_host_pattern)
            docker_installation_job = ansible.ansible_playbook.install_docker()
            await docker_installation_job
        except IgnoredAnsibleFailure:
            raise RuntimeError("Unable to install Docker")

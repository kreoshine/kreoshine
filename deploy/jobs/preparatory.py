"""
Job that make preparation before deployment
"""
import asyncio
import logging
import os

from ansible import AnsibleExecutor
from deploy.deploy_const import PROJECT_ROOT_PATH, PRODUCTION_MODE, DEVELOPMENT_MODE
from settings import config, SETTINGS_ROOT_PATH

logger = logging.getLogger('ansible_deploy')

# pylint: disable = fixme


async def make_preparation(ansible: AnsibleExecutor):
    """
    Performs pre-deployment jobs regarding the project and in dependency of the deployment mode
    """
    deploy_mode = config.deploy.mode

    if deploy_mode == DEVELOPMENT_MODE:
        # make available absolute project path in deployment
        config.server.project_root_path = PROJECT_ROOT_PATH
    # else: no need to define project directory for production — it should be used from configuration

    if deploy_mode == PRODUCTION_MODE:
        # be sure that user admin existing — his home directory will be used for project location
        admin_creation_task = asyncio.create_task(
            ansible.ansible_module.create_user(user_name=config.server.admin.user_name,
                                               privilege_escalation_group=config.server.admin.sudo_group))
        await admin_creation_task  # fixme: need sudo permissions
        # todo: clone repository to admin home dir

    logger.debug("Define '%s' environment for dynaconf: %s", deploy_mode, os.path.join(SETTINGS_ROOT_PATH, '.env'))
    dote_env_content = f'export KREOSHINE_ENV={deploy_mode.upper()}'
    env_creation_task = asyncio.create_task(ansible.ansible_playbook.create_file(target_dir=SETTINGS_ROOT_PATH,
                                                                                 file_name='.env',
                                                                                 file_content=dote_env_content))
    await env_creation_task


async def install_docker(ansible: AnsibleExecutor):
    """ Installs Docker
    Args:
        ansible: instance of ansible executor
        """
    # todo: install docker
    logger.debug("Installation docker on %s host", ansible.target_host_pattern)

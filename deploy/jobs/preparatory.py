"""
Job that make preparation before deployment
"""
import asyncio
import logging
import os
from pathlib import Path

from ansible import AnsibleExecutor
from deploy import PRODUCTION_MODE, DEVELOPMENT_MODE
from settings import config, SETTINGS_DIR

logger = logging.getLogger('ansible_deploy')


async def make_preparation(ansible: AnsibleExecutor):
    """
    Performs pre-deployment jobs regarding the project and in dependency of the deployment mode
    """
    deploy_mode = config.deploy.mode
    if deploy_mode == PRODUCTION_MODE:
        admin_creation_task = asyncio.create_task(
            ansible.ansible_module.create_user(user_name=config.server.admin.user_name,
                                               privilege_escalation_group=config.server.admin.sudo_group))
        await admin_creation_task  # fixme: need sudo permissions
        # todo: clone repository to admin home dir

    if deploy_mode == DEVELOPMENT_MODE:
        settings_directory = SETTINGS_DIR
        # make available absolute project path in deployment
        config.server.project_root_path = str(Path(__file__).parent.parent.resolve())
    else:  # deploy_mode == PRODUCTION_MODE
        settings_directory = os.path.join(config.server.project_root_path, 'settings')
        # be sure that user admin existing

    logger.debug(f"Define '{deploy_mode}' environment for dynaconf: {os.path.join(settings_directory, '.env')}")
    dote_env_content = f'export KREOSHINE_ENV={deploy_mode.upper()}'
    env_creation_task = asyncio.create_task(ansible.ansible_playbook.create_file(target_dir=settings_directory,
                                                                                 file_name='.env',
                                                                                 file_content=dote_env_content))
    await env_creation_task


async def install_docker(ansible: AnsibleExecutor):
    # todo: install docker
    pass

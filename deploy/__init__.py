"""
Package for deployment
"""
import asyncio
import logging.config
import logging
import os
from pathlib import Path

from ansible import AnsibleExecutor
from settings import config, SETTINGS_DIR

logger = logging.getLogger('ansible_deploy')

# allowed deployment modes
DEVELOPMENT_MODE = 'development'
PRODUCTION_MODE = 'production'


def configure_deploy_logging_locally(logger_file: str):
    """
    Configures deploy logging file locally

    Args:
        logger_file: path of the logger file (expected that directory to this file is already exist)
    """
    deploy_log_config = config.logging_ansible_deploy
    if not deploy_log_config['handlers']['service_file']['filename']:
        deploy_log_config['handlers']['service_file']['filename'] = logger_file
    logging.config.dictConfig(config=deploy_log_config)


async def prepare_project_for_deployment(ansible: AnsibleExecutor):
    """
    Performs pre-deployment tasks regarding the project and in dependency of the deployment mode
    """
    deploy_mode = config.deploy.mode
    if deploy_mode == DEVELOPMENT_MODE:
        settings_directory = SETTINGS_DIR
        # make available absolute project path in deployment
        config.server.project_root_path = str(Path(__file__).parent.parent.resolve())
    else:  # deploy_mode == PRODUCTION_MODE
        settings_directory = os.path.join(config.server.project_root_path, 'settings')
        # be sure that user admin existing
        admin_creation_task = asyncio.create_task(
            ansible.execute_user_creation_task(user_name=config.server.admin.user_name,
                                               privilege_escalation_group=config.server.admin.sudo_group))
        await admin_creation_task  # fixme: need sudo permissions
        # todo: clone repository to admin home dir

    logger.debug(f"Define '{deploy_mode}' environment for dynaconf: {os.path.join(settings_directory, '.env')}")
    dote_env_content = f'export KREOSHINE_ENV={deploy_mode.upper()}'
    env_creation_task = asyncio.create_task(ansible.execute_file_create_task(target_dir=settings_directory,
                                                                             file_name='.env',
                                                                             file_content=dote_env_content))
    await env_creation_task


async def install_docker(ansible: AnsibleExecutor):
    # todo: install docker
    pass


async def configure_nginx(ansible: AnsibleExecutor) -> None:
    """ Configures nginx
    Args:
        ansible: instance of ansible executor
    """


async def perform_deployment(deploy_mode: str, local_output_dir: str):
    """
    Deployment entry point

    Args:
        deploy_mode: mode of deployment
        local_output_dir: path to an existing local directory to be used:
                              - for deployment log files
                              - as ansible-runner's private data directory
    """
    configure_deploy_logging_locally(logger_file=os.path.join(local_output_dir, 'ansible-deploy.log'))

    assert deploy_mode in (PRODUCTION_MODE, DEVELOPMENT_MODE), \
        f"Only two modes of deployment is allowed: '{DEVELOPMENT_MODE}' and '{PRODUCTION_MODE}'"

    target_host = config.server.ip
    logger.info(f"Initiate '{deploy_mode}' mode of deployment on '{target_host}' host")

    ansible_executor = AnsibleExecutor(destination_host=target_host,
                                       private_data_dir=local_output_dir,
                                       verbosity=config.ansible.verbosity)
    logger.debug(f"Successfully initiate instance of 'ansible executor' class")

    echo_task = asyncio.create_task(ansible_executor.execute_echo_task(need_gather_facts=False))
    await echo_task
    logger.info(f"Connection to {ansible_executor.target_host} host available")

    logger.debug("Preparing the project for deployment")
    await prepare_project_for_deployment(ansible=ansible_executor)

    logger.debug("Docker installation")
    await install_docker(ansible=ansible_executor)

    logger.debug("Configure Nginx as a web-server")
    await configure_nginx(ansible=ansible_executor)

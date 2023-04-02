"""
Package for deployment
"""
import asyncio
import logging.config
import logging
import os

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

    ansible = AnsibleExecutor(destination_host=target_host,
                              private_data_dir=local_output_dir,
                              verbosity=config.ansible.verbosity)
    logger.debug(f"Successfully initiate instance of 'ansible executor' class")

    echo_task = asyncio.create_task(ansible.execute_echo_task(need_gather_facts=False))
    await echo_task
    logger.info(f"Connection to {ansible.target_host} host available")

    logger.debug(f"Define '{deploy_mode}' environment for dynaconf: {os.path.join(SETTINGS_DIR, '.env')}")
    dote_env_content = f'export KREOSHINE_ENV={deploy_mode.upper()}'
    env_creation_task = asyncio.create_task(ansible.execute_file_create_task(target_dir=SETTINGS_DIR,
                                                                             file_name='.env',
                                                                             file_content=dote_env_content))
    await env_creation_task

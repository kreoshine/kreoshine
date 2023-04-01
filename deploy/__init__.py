"""
Package for deployment
"""
import asyncio
import logging.config
import logging
import os
from os import makedirs
from pathlib import Path

from ansible import AnsibleExecutor
from settings import config, SETTINGS_DIR

logger = logging.getLogger('ansible_deploy')

PROJECT_DIR = str(Path(__file__).parent.parent.resolve())
TEMPORARY_DIR = os.path.join(PROJECT_DIR, 'tmp/')

# allowed deployment modes
DEVELOPMENT_MODE = 'development'
PRODUCTION_MODE = 'production'


def create_directory(dir_path: str):
    """ Creates a directory on the path if it is not created """
    try:
        makedirs(dir_path)
        print(f"Directory {dir_path} successfully created")
    except FileExistsError:
        print(f"Directory {dir_path} already exist")
        pass


def configure_deploy_logging_locally(logger_file: str):
    """
    Configures deploy logging file locally

    Args:
        logger_file: path of the logger file (expected that directory to this file is already exist)
    """
    deploy_log_config = config.logging_ansible_deploy
    deploy_log_config['handlers']['service_file']['filename'] = logger_file
    logging.config.dictConfig(config=deploy_log_config)


async def init_deploy():
    """ Entry point for deployment initialization """
    create_directory(dir_path=TEMPORARY_DIR)
    configure_deploy_logging_locally(logger_file=os.path.join(TEMPORARY_DIR, 'ansible-deploy.log'))

    deploy_mode = config.deploy.mode
    assert deploy_mode in (PRODUCTION_MODE, DEVELOPMENT_MODE), \
        f"Only two modes of deployment is allowed: '{DEVELOPMENT_MODE}' and '{PRODUCTION_MODE}'"

    target_host = config.server.ip
    logger.info(f"Initiate '{deploy_mode}' mode of deployment on '{target_host}' host")

    ansible = AnsibleExecutor(destination_host=target_host,
                              private_data_dir=TEMPORARY_DIR,
                              verbosity=config.ansible.verbosity)
    logger.debug(f"Successfully initiate instance of 'ansible executor' class")

    echo_task = asyncio.create_task(ansible.execute_echo_task(need_gather_facts=False))
    await echo_task
    logger.info(f"Connection to {ansible.target_host} host available")

    logger.debug(f"Define 'dev' environment for dynaconf: {os.path.join(SETTINGS_DIR, '.env')}")
    dote_env_content = 'export KREOSHINE_ENV=DEVELOPMENT'
    env_creation_task = asyncio.create_task(ansible.execute_file_create_task(target_dir=SETTINGS_DIR,
                                                                             file_name='.env',
                                                                             file_content=dote_env_content))
    await env_creation_task

"""
Package for deployment
"""
import logging.config
import logging
import os
from os import makedirs
from pathlib import Path

from ansible import AnsibleExecutor, ANSIBLE_PRIVATE_DATA_DIR
from deploy.dev import process_dev_deploy
from settings import config

logger = logging.getLogger('ansible_deploy')

PROJECT_DIR = str(Path(__file__).parent.parent.resolve())
TEMPORARY_DIR = os.path.join(PROJECT_DIR, 'tmp/')

# allowed deployment modes
DEVELOPMENT_MODE = 'development'
PRODUCTION_MODE = 'production'


def create_ansible_dir_locally():
    """ Creates directories in project dir (i.e. tmp/ansible) """
    try:
        makedirs(ANSIBLE_PRIVATE_DATA_DIR)
        print(f"Directory {ANSIBLE_PRIVATE_DATA_DIR} successfully created")
    except FileExistsError:
        print(f"Directory {ANSIBLE_PRIVATE_DATA_DIR} already exist")
        pass


def configure_deploy_log_file_locally():
    """
    Configures deploy logging file locally
    """
    create_ansible_dir_locally()
    ansible_log_config = config.logging_ansible_deploy
    ansible_log_config['handlers']['service_file']['filename'] = os.path.join(TEMPORARY_DIR, 'ansible-deploy.log')
    logging.config.dictConfig(config=ansible_log_config)


async def init_deploy():
    """ Entry point for deployment initialization """
    configure_deploy_log_file_locally()

    deploy_mode = config.deploy.mode
    assert deploy_mode in (PRODUCTION_MODE, DEVELOPMENT_MODE), \
        f"Only two modes of deployment is allowed: '{DEVELOPMENT_MODE}' and '{PRODUCTION_MODE}'"

    target_host = config.server.ip
    logger.info(f"Initiate '{deploy_mode}' mode of deployment on '{target_host}' host")

    ansible_executor = AnsibleExecutor(destination_host=target_host)
    logger.debug(f"Successfully initiate instance of 'ansible executor' class")

    if deploy_mode == DEVELOPMENT_MODE:
        await process_dev_deploy(ansible=ansible_executor)

"""
Package for deployment
"""
import logging.config
import logging
import os

from ansible import AnsibleExecutor
from deploy.modes import DEVELOPMENT_MODE, PRODUCTION_MODE
from deploy.jobs import *
from settings import config

logger = logging.getLogger('ansible_deploy')


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

    ansible_executor = AnsibleExecutor(host_pattern=target_host,
                                       private_data_dir=local_output_dir,
                                       verbosity=config.ansible.verbosity)
    logger.debug(f"Successfully initiate instance of '{AnsibleExecutor.__name__}' class")

    await echo_host(ansible=ansible_executor, need_gather_facts=deploy_mode == PRODUCTION_MODE)
    logger.info(f"Connection to {ansible_executor.target_host_pattern} host available")

    logger.debug("Preparing the project for deployment")
    await make_preparation(ansible=ansible_executor)

    logger.debug("Docker installation")
    await install_docker(ansible=ansible_executor)

    logger.debug("Configure Nginx as a web-server")
    await configure_nginx(ansible=ansible_executor)

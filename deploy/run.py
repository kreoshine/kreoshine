"""
Automatic deployment with Ansible and ansible-runner
"""
import asyncio
import logging
import logging.config
import os

from concurrent.futures import ThreadPoolExecutor

from deploy import perform_deployment
from deploy.deploy_const import PROJECT_ROOT_PATH
from settings import config


def configure_deploy_logging_locally(logger_file: str):
    """
    Configures deploy logging file locally

    Args:
        logger_file: path of the logger file
    """
    dir_path = os.path.dirname(logger_file)
    try:
        os.makedirs(dir_path)
        print(f"Directory {dir_path} successfully created")
    except FileExistsError:
        print(f"Directory {dir_path} already exist")

    deploy_log_config = config.logging_ansible_deploy
    if not deploy_log_config['handlers']['service_file']['filename']:
        deploy_log_config['handlers']['service_file']['filename'] = logger_file
    logging.config.dictConfig(config=deploy_log_config)


if __name__ == '__main__':
    configure_deploy_logging_locally(logger_file=os.path.join(PROJECT_ROOT_PATH.joinpath('tmp/'), 'ansible-deploy.log'))

    asyncio.new_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=2))
    asyncio.run(
        perform_deployment(deploy_mode=config.deploy.mode,
                           local_output_dir=PROJECT_ROOT_PATH.joinpath('tmp/ansible'))
    )

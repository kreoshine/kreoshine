"""
Package is responsible for deployment in different modes.
"""
import os
from pathlib import Path

from deploy.ansible import AnsibleExecutor
from deploy.deployment.dev import process_dev_deploy
from deploy.deployment.utils import create_ansible_dir_locally
from settings import config

PROJECT_DIR = str(Path(__file__).parent.parent.resolve())
TEMPORARY_DIR = os.path.join(PROJECT_DIR, 'tmp/')

# allowed deployment modes
DEVELOPMENT_MODE = 'development'
PRODUCTION_MODE = 'production'


async def init_deploy():
    """ Entry point for deployment initialization """
    create_ansible_dir_locally()

    deploy_mode = config.deploy.mode

    assert deploy_mode in (PRODUCTION_MODE, DEVELOPMENT_MODE), \
        f"Only two modes of deployment is allowed: '{DEVELOPMENT_MODE}' and '{PRODUCTION_MODE}'"
    target_host = config.server.ip
    print(f"Initiate '{deploy_mode}' mode of deployment on '{target_host}' host")

    ansible_executor = AnsibleExecutor(destination_host=target_host)
    print(f"Successfully initiate instance of 'ansible executor' class")

    if deploy_mode == DEVELOPMENT_MODE:
        await process_dev_deploy(ansible=ansible_executor)

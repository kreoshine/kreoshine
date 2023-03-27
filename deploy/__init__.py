"""
Package for deployment
"""
import asyncio

from deploy.ansible import AnsibleExecutor
from deploy.deployment import DEVELOPMENT_MODE, PRODUCTION_MODE
from deploy.deployment.modes.development import process_dev_deploy
from deploy.settings import config


async def init_deploy():
    """ Entry point for deployment initialization """
    deploy_mode = config.deploy_mode

    assert deploy_mode in (PRODUCTION_MODE, DEVELOPMENT_MODE), \
        f"Only two modes of deployment is allowed: '{DEVELOPMENT_MODE}' and '{PRODUCTION_MODE}'"
    target_host = config.server.ip
    print(f"Initiate '{deploy_mode}' mode of deployment on '{target_host}' host")

    ansible_executor = AnsibleExecutor(destination_host=target_host)
    print(f"Successfully initiate instance of 'ansible executor' class")

    echo_task = asyncio.create_task(ansible_executor.execute_echo_task())
    await echo_task
    print(f"Connection to {target_host} host available")

    if deploy_mode == DEVELOPMENT_MODE:
        await process_dev_deploy(ansible=ansible_executor)

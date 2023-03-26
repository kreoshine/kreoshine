"""
Automatic deployment with Ansible and ansible-runner
"""
import asyncio

from concurrent.futures import ThreadPoolExecutor

from ansible import AnsibleExecutor
from deployment import DEVELOPMENT_MODE, PRODUCTION_MODE
from deployment.modes.development import process_dev_deploy
from deployment.utils import create_ansible_dir_locally

from settings import config


async def init_deploy():
    """ Entry point for deployment initialization """
    deploy_mode = config.deploy_mode
    if deploy_mode == DEVELOPMENT_MODE:
        target_host = 'localhost'  # fixme: here should be just local — unable to read 'hosts' file
    else:
        assert deploy_mode == PRODUCTION_MODE, \
            f"Only two modes of deployment is allowed: '{DEVELOPMENT_MODE}' and '{PRODUCTION_MODE}'"
        target_host = 'remote'
    print(f"Initiate '{deploy_mode}' mode of deployment")
    ansible_executor = AnsibleExecutor(destination_host=target_host)
    print(f"Successfully initiate instance of 'ansible executor' class for the '{target_host}' host")

    echo_task = asyncio.create_task(ansible_executor.execute_echo_task())
    await echo_task
    print(f"Connection to {target_host} host available")

    if deploy_mode == DEVELOPMENT_MODE:
        await process_dev_deploy(ansible=ansible_executor)


if __name__ == '__main__':
    create_ansible_dir_locally()
    asyncio.new_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=2))
    asyncio.run(init_deploy())

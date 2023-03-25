"""
Automatic deployment with Ansible and ansible-runner
"""
import asyncio
from os import makedirs

from concurrent.futures import ThreadPoolExecutor

from deploy.ansible import ANSIBLE_PRIVATE_DATA_DIR, AnsibleExecutor
from settings import config

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


async def init_deploy():
    """ Entry point for deployment initialization """
    deploy_mode = config.deploy_mode
    if deploy_mode == DEVELOPMENT_MODE:
        target_host = 'local'
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


if __name__ == '__main__':
    create_ansible_dir_locally()
    asyncio.new_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=2))
    asyncio.run(init_deploy())

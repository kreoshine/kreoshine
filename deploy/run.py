"""
Automatic deployment with Ansible and ansible-runner
"""
import asyncio

from concurrent.futures import ThreadPoolExecutor

from deploy import init_deploy
from deployment.utils import create_ansible_dir_locally


if __name__ == '__main__':
    create_ansible_dir_locally()
    asyncio.new_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=2))
    asyncio.run(init_deploy())

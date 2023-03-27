"""
Automatic deployment with Ansible and ansible-runner
"""
import asyncio

from concurrent.futures import ThreadPoolExecutor

from deploy import init_deploy


if __name__ == '__main__':
    asyncio.new_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=2))
    asyncio.run(init_deploy())

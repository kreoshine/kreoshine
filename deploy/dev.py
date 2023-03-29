"""
Module is responsible for deployment in development mode.
"""
import asyncio
import logging
import os
from pathlib import Path

from ansible import AnsibleExecutor
from settings import DYNACONF_ROOT_PATH

logger = logging.getLogger('ansible_deploy')

TEMPORARY_DIR = os.path.join(str(Path(__file__).parent.parent.parent.parent.resolve()), 'tmp/')


async def process_dev_deploy(ansible: AnsibleExecutor) -> None:
    """
    Entry point of deployment for the dev needs

    Args:
        ansible: instance of AnsibleExecutor class
    """
    echo_task = asyncio.create_task(ansible.execute_echo_task(need_gather_facts=False))
    await echo_task
    logger.info(f"Connection to {ansible.target_host} host available")

    print(f"Define 'dev' environment for dynaconf: {os.path.join(DYNACONF_ROOT_PATH, '.env')}")
    dote_env_content = 'export KREOSHINE_ENV=DEVELOPMENT'
    env_creation_task = asyncio.create_task(ansible.execute_file_create_task(target_dir=DYNACONF_ROOT_PATH,
                                                                             file_name='.env',
                                                                             file_content=dote_env_content))
    await env_creation_task

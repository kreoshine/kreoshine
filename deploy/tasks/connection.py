"""

"""
import asyncio
import logging

from ansible import AnsibleExecutor

logger = logging.getLogger('ansible_deploy')


async def echo_host(ansible: AnsibleExecutor, need_gather_facts: bool):

    echo_task = asyncio.create_task(ansible.ansible_playbook.echo(need_gather_facts=need_gather_facts))
    await echo_task
    logger.info(f"Connection to {ansible.target_host_pattern} is available")

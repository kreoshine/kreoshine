"""
Job that ensure connection
"""
import asyncio
import logging

from ansible import AnsibleExecutor

logger = logging.getLogger('ansible_deploy')


async def echo_host(ansible: AnsibleExecutor, need_gather_facts: bool):
    """ Executes echo playbook
    Args:
        ansible: instance of ansible executor
        need_gather_facts: gather facts neediness
    """

    echo_task = asyncio.create_task(ansible.ansible_playbook.echo(need_gather_facts=need_gather_facts))
    await echo_task
    logger.info("Connection to %s is available", ansible.target_host_pattern)

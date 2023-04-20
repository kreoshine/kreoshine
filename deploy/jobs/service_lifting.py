"""
Jobs that lift different services
"""
import logging

from ansible import AnsibleExecutor

logger = logging.getLogger('ansible_deploy')


async def init_nginx_container(ansible: AnsibleExecutor) -> None:
    """ Configures nginx
    Args:
        ansible: instance of ansible executor
    """
    logger.debug("Nginx configuration on a %s host", ansible.target_host_pattern)
    nginx_initialization_task = ansible.ansible_roles.execute_nginx_role()
    await nginx_initialization_task
    logger.info("Successfully create nginx container")

"""
Jobs that lift different services
"""
import logging

from ansible import AnsibleExecutor

logger = logging.getLogger('ansible_deploy')


async def configure_nginx(ansible: AnsibleExecutor) -> None:
    """ Configures nginx
    Args:
        ansible: instance of ansible executor
    """
    # pylint: disable = fixme
    # todo: install and configure nginx
    logger.debug("Nginx configuration on a %s host", ansible.target_host_pattern)

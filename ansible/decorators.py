"""
Module with decorators for ansible
"""
import logging
from typing import Callable

from ansible.exceptions import KnownAnsibleError

logger = logging.getLogger('ansible_deploy')


def error_log_handler(func: callable) -> Callable:
    """ An error handling decorator for logging that can be used for asynchronous ansible executor methods """
    async def wrapped(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except KnownAnsibleError as err:
            logger.error(err)
            if err.error_output:
                logger.error(err.error_output)
            raise
    return wrapped

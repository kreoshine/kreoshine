"""
Module with decorators for ansible
"""
import logging
from functools import wraps
from typing import Callable

from ansible.exceptions import KnownAnsibleError, AnsibleExecuteError

logger = logging.getLogger('ansible_deploy')


# pylint: disable = missing-return-doc
def error_log_handler(_func: callable = None, *,
                      trace_unexpected_error: bool = True,
                      refuse_execute_error_logging: bool = False) -> Callable:
    """ An error handling decorator for logging that can be used for asynchronous ansible executor methods
    Args:
        _func: parameter implemented to allow the decorator to be called without parameters
            Note: should never be used to pass an argument!
        trace_unexpected_error: neediness to trace unexpected error;
            if set to True, there is a traceback of unexpected exception for logging
        refuse_execute_error_logging: neediness to log 'execute' error;

    Notes: the parameters can only be used to pass named arguments!
    """
    def decorator(func: callable):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as err:  # pylint: disable = broad-except
                # pylint: disable = no-member
                if isinstance(err, KnownAnsibleError):
                    if isinstance(err, AnsibleExecuteError) and refuse_execute_error_logging:
                        logger.warning("Error logging was rejected")
                        raise
                    logger.error(err)
                    if err.error_output:
                        logger.error(err.error_output)
                else:
                    if trace_unexpected_error:
                        logger.exception("Unexpected error")
                raise
        return wrapped

    if _func is None:  # decorator called with param
        return decorator
    # decorator called without param
    return decorator(_func)

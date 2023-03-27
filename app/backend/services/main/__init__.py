"""
Main KreoShine service
"""
import logging
import logging.config
import sys

from concurrent.futures import ThreadPoolExecutor

import asyncio
from aiohttp import web

from settings import config

logger = logging.getLogger('app')


async def on_app_start(app):
    """
    Service initialization on application start

    Args:
        app: instance of the application
    """
    service_config = app['service_config']
    asyncio.get_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=service_config['thread_pool_size']))

    logger.info('Init Database engine')
    # todo: implement database initialization


async def on_app_stop(app) -> None:
    """
    Stops tasks on the application destroy

    Args:
        app: instance of the application
    """
    # todo: set log file path for 'service.log' as empty string


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    """ Handler for uncaught exceptions """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception!", exc_info=(exc_type, exc_value, exc_traceback))


def create_app(service_config: dict) -> web.Application:
    """
    Creates web application

    Args:
        service_config: configuration for service
    """
    logging.config.dictConfig(config=config.logging)
    sys.excepthook = handle_exception

    app = web.Application(client_max_size=service_config['client_max_size'])
    app['service_config'] = service_config
    app.on_startup.append(on_app_start)
    app.on_shutdown.append(on_app_stop)

    return app

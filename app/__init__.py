"""
Asynchronous python application based on aiohttp-framework with REST-API architecture
"""
import logging
import logging.config
import sys

from concurrent.futures import ThreadPoolExecutor

import asyncio
from aiohttp import web

from settings import settings

logger = logging.getLogger('app')


async def on_app_start(app):
    """
    Service initialization on application start

    Args:
        app: instance of the application
    """
    asyncio.get_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=settings.app['thread_pool_size']))

    logger.info('Init Database engine')
    # todo: implement database initialization


async def on_app_stop(app) -> None:
    """
    Stops tasks on the application destroy

    Args:
        app: instance of the application
    """
    pass


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    """ Handler for uncaught exceptions """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception!", exc_info=(exc_type, exc_value, exc_traceback))


def create_app() -> web.Application:
    """
    Creates web application.
    """
    logging.config.dictConfig(config=settings.logging)  # fixme: resolve path — /var/log/kreoshine/service.log
    sys.excepthook = handle_exception

    app = web.Application(client_max_size=settings.app['client_max_size'])
    app.on_startup.append(on_app_start)
    app.on_shutdown.append(on_app_stop)

    return app

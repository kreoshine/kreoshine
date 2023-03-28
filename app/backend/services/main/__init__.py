"""
Main KreoShine service
"""
import logging.config

from concurrent.futures import ThreadPoolExecutor

import asyncio
from aiohttp import web

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


def create_app(service_config: dict) -> web.Application:
    """
    Creates web application

    Args:
        service_config: configuration for service
    """
    app = web.Application(client_max_size=service_config['client_max_size'])
    app['service_config'] = service_config
    app.on_startup.append(on_app_start)
    app.on_shutdown.append(on_app_stop)

    return app

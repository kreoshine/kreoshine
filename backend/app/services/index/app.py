"""
Index application
"""
import logging.config
import asyncio
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import aiohttp_cors
from aiohttp import web

from api.view import IndexView
from settings import config

logger = logging.getLogger('index_service')


async def on_app_start(app):
    """ Service initialization on application start """
    service_config = config.app.services.index
    asyncio.get_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=service_config['thread_pool_size']))

    logger.info("Service 'index' successfully started")


async def on_app_stop(app) -> None:
    """ Stops tasks on the application destroy """


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    """ Handler for uncaught exceptions for 'main_service' logger """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception!", exc_info=(exc_type, exc_value, exc_traceback))


def configure_logging(logging_config: dict) -> None:
    """ Configures logging for 'main_service' service """
    if config.deploy.mode == 'development':
        project_root_dir = Path(os.path.abspath(__file__)).parent.parent.parent.parent.parent.resolve()
        logging_config['handlers']['service_file']['filename'] = os.path.join(project_root_dir, 'tmp/index-service.log')
    logging.config.dictConfig(config=logging_config)
    sys.excepthook = handle_exception


def create_index_service() -> web.Application:
    """ Creates instance of web application for 'index' service """
    configure_logging(logging_config=config.logging_index_service)

    app = web.Application(client_max_size=config.app.services.index['client_max_size'])

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    cors.add(app.router.add_route('GET', '/index', IndexView))

    app.on_startup.append(on_app_start)
    app.on_shutdown.append(on_app_stop)

    logger.debug("Instance of application for 'index' service successfully created")
    return app

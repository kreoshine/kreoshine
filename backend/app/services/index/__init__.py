"""
Index application
"""
import logging
import logging.config
import asyncio
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import aiohttp_cors
from aiohttp import web

from api.view import IndexView
from settings import config

logger = logging.getLogger('index_service')


async def on_service_start(app):
    """ Initialization of 'index' service """
    service_config = config.app.services.index
    asyncio.get_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=service_config['thread_pool_size']))

    logger.info("Service 'index' successfully started")


async def on_service_stop(app) -> None:
    """ Stops tasks when the service is destroyed """


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    """ Handler for uncaught exceptions for logger of 'index' service """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception!", exc_info=(exc_type, exc_value, exc_traceback))


def configure_logging(logging_config: dict) -> None:
    """ Configures logging for 'index' service """
    if config.deploy.mode == 'development':
        project_root_dir = Path(os.path.abspath(__file__)).parent.parent.parent.parent.parent.resolve()
        logging_config['handlers']['service_file']['filename'] = os.path.join(project_root_dir, 'tmp/index-service.log')
    logging.config.dictConfig(config=logging_config)
    sys.excepthook = handle_exception


def create_index_service() -> web.Application:
    """ Creates instance of web application for 'index' service """
    configure_logging(logging_config=config.logging_index_service)

    service = web.Application(client_max_size=config.app.services.index['client_max_size'])

    cors = aiohttp_cors.setup(service, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    cors.add(service.router.add_route('GET', '/index', IndexView))

    service.on_startup.append(on_service_start)
    service.on_shutdown.append(on_service_stop)

    logger.debug("Instance of web-application for 'index' service successfully created")
    return service

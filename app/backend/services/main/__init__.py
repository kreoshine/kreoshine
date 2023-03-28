"""
Main KreoShine service
"""
import logging
import logging.config
import os
import sys

from concurrent.futures import ThreadPoolExecutor

import asyncio
import aiohttp_cors
from aiohttp import web

from app.backend.services.main.api import ExampleView
from deploy import DEVELOPMENT_MODE, TEMPORARY_DIR
from settings import config

logger = logging.getLogger('main_service')


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    """ Handler for uncaught exceptions for 'main_service' logger """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception!", exc_info=(exc_type, exc_value, exc_traceback))


def configure_logging(logging_config: dict) -> None:
    """ Configures logging for 'main_service' service """
    if config.deploy.mode == DEVELOPMENT_MODE:
        logging_config['handlers']['service_file']['filename'] = os.path.join(TEMPORARY_DIR, 'main-service.log')
    logging.config.dictConfig(config=logging_config)
    sys.excepthook = handle_exception


async def on_app_start(app):
    """ Service initialization on application start """
    service_config = config.app.services.main
    asyncio.get_event_loop().set_default_executor(ThreadPoolExecutor(max_workers=service_config['thread_pool_size']))

    logger.debug('Initialize database engine')
    # todo: implement database initialization (if need)
    logger.info("Service 'main' successfully started")


async def on_app_stop(app) -> None:
    """ Stops tasks on the application destroy """


def create_main_app() -> web.Application:
    """ Creates instance of web application for 'main' service """
    configure_logging(logging_config=config.logging_main_service)

    app = web.Application(client_max_size=config.app.services.main['client_max_size'])

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    cors.add(app.router.add_route('GET', '/', ExampleView))

    app.on_startup.append(on_app_start)
    app.on_shutdown.append(on_app_stop)

    logger.debug("Instance of application for 'main' service successfully created")
    return app

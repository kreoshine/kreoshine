"""
Service running module
"""
import logging
import logging.config
import os.path
import sys

from aiohttp import web

from app.backend.services.main import create_app
from deploy import DEVELOPMENT_MODE
from deploy.deployment import TEMPORARY_DIR
from settings import config

logger = logging.getLogger('app')


def handle_exception(exc_type, exc_value, exc_traceback) -> None:
    """ Handler for uncaught exceptions """
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught exception!", exc_info=(exc_type, exc_value, exc_traceback))


def configure_logging(service_config: dict, ):
    """ Configures logging for main service """
    if config.deploy.mode == DEVELOPMENT_MODE:
        service_config['handlers']['service_file']['filename'] = os.path.join(TEMPORARY_DIR, 'main-service.log')
    logging.config.dictConfig(config=service_config)
    sys.excepthook = handle_exception


if __name__ == '__main__':
    configure_logging(service_config=dict(config.logging.main_service))

    main_service_config = dict(config.app.services.main)
    main_service = create_app(service_config=main_service_config)
    web.run_app(main_service,
                host=main_service_config['host'],
                port=main_service_config['port'],
                access_log_format=config.app['access_log_format'])

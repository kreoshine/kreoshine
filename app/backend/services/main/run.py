"""
Service running module
"""
from aiohttp import web

from app.backend.services.main import create_app
from settings import config


if __name__ == '__main__':
    main_service_config = dict(config.app.services.main)
    service_log_config = dict(config.logging.main_service)
    main_service = create_app(service_config=main_service_config,
                              log_config=service_log_config)
    web.run_app(main_service,
                host=main_service_config['host'],
                port=main_service_config['port'],
                access_log_format=config.app['access_log_format'])

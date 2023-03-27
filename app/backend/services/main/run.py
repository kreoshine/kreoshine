"""
Service running module
"""
from aiohttp import web

from app.backend.services.main import create_app
from settings import config


if __name__ == '__main__':
    main_service_config = dict(config.app.services.main)
    main_service = create_app(service_config=main_service_config)
    web.run_app(main_service,
                host=main_service_config['host'],
                port=main_service_config['port'],
                access_log_format=config.app['access_log_format'])

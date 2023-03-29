"""
Service running module
"""
from aiohttp import web

from app import create_index_service
from settings import config


if __name__ == '__main__':
    service_config = config.app.services.index
    service = create_index_service()
    web.run_app(service,
                host=service_config['host'],
                port=service_config['port'],
                access_log_format=config.app['access_log_format'])

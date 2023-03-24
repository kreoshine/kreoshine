"""
Service running module
"""
from aiohttp import web

from app import create_app
from settings import config


if __name__ == '__main__':
    app = create_app()
    web.run_app(app,
                host=config.app['host'],
                port=config.app['port'],
                access_log_format=config.app['access_log_format'])

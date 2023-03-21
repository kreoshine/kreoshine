"""
Service running module
"""
from aiohttp import web

from app import create_app
from settings import settings


if __name__ == '__main__':
    app = create_app()
    web.run_app(app,
                host=settings.app['host'],
                port=settings.app['port'],
                access_log_format=settings.app['access_log_format'])

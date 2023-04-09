"""
Implementation of the 'index' endpoint
"""
import logging

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from aiohttp.web_urldispatcher import View
from aiohttp_cors import CorsViewMixin

from api import const

logger = logging.getLogger('main_service')


class IndexView(View, CorsViewMixin):
    """ Example view """

    async def get(self) -> Response:
        """ Handler for GET request """
        return await self._process_get(self.request)

    async def _process_get(self, request: Request) -> Response:
        logger.debug("Got request: %s", request)
        response_dict = {
            const.STATUS_CODE: 200,
            const.BODY: {}
        }
        logger.debug("Send response: %s", response_dict)
        return web.json_response(response_dict)

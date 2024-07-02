import aiohttp

from .exceptions import KabuStationApiException


class RestAPIClient(object):
    def __init__(self):
        self.token = None
        self.endpoint = ''

    @staticmethod
    async def _request(method, url, **kwargs):
        async with aiohttp.ClientSession() as session:
            async with session.request(method=method, url=url, **kwargs) as response:
                resp_json = await response.json()
                return resp_json

    async def get_token(self, password):
        method = 'POST'
        path = ''
        body = {"APIPassword": password}
        resp_json = await self._request(method=method, url=self.endpoint+path, body=body)
        if resp_json['ResultCode'] != 0:
            raise KabuStationApiException()
        self.token = resp_json['Token']

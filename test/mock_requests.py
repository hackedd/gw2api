import urllib
import requests
from StringIO import StringIO


class MockSession(object):
    def __init__(self):
        super(MockSession, self).__init__()
        self.responses = {}

    def add_params(self, url, params):
        if not params:
            return url

        if isinstance(params, dict):
            params = params.items()

        return url + "?" + urllib.urlencode(sorted(params))

    def get_mock_response(self, method, url, params=None):
        url = self.add_params(url, params)

        if method in self.responses and url in self.responses[method]:
            response_data = self.responses[method][url]
        else:
            response_data = self.responses.get(url)

        response = requests.Response()

        if response_data is None:
            response.status_code = 404
            response.reason = url + " not found"
        else:
            response.status_code = 200
            response.raw = StringIO(response_data)

        return response

    def add_mock_response(self, method, url, response, params=None):
        url = self.add_params(url, params)

        if method:
            if method not in self.responses:
                self.responses[method] = {}
            self.responses[method][url] = response
        else:
            self.responses[url] = response

    def get(self, url, **kwargs):
        return self.get_mock_response("get", url, kwargs.get("params"))

    def post(self, url, **kwargs):
        return self.get_mock_response("post", url, kwargs.get("params"))

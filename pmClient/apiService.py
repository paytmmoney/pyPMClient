import requests
import json
from .enums import Requests
from .constants import Constants


class ApiService(Constants):
    def __init__(self):
        Constants.__init__(self)

    def api_call_helper(self, name, http_method, params, data):
        """helper formats the url and reads error codes nicely"""
        config = self._service_config
        url = f"{config['host']}{config['routes'][name]}"
        if params is not None:
            url = url.format(**params)
        response = self._api_call(url, http_method, data)
        if response.status_code != 200:
            if response.status_code == 400:
                raise AttributeError(response.text)
            elif response.status_code == 404:
                raise Exception(response.text)
            elif response.status_code == 415:
                raise Exception(response.text)
            elif response.status_code == 500:
                raise Exception(response.text)
            elif response.status_code == 401:
                raise ConnectionError(response.text)
            else:
                raise requests.HTTPError(response.text, response.status_code)
        if name == "security_master":
            return response.text
        else:
            return json.loads(response.text)

    def _api_call(self, url, http_method, data):
        """Checks for the API Method and that call is done and returned"""
        config = self._service_config
        if url == f"{config['host']}{config['routes']['security_master']}":
            headers = {"Content-Type": "application/vnd.ms-excel"}
        else:
            headers = {"Content-Type": "application/json"}
        if self.access_token is not None:
            headers['x-jwt-token'] = self.access_token
        r = None
        if http_method is Requests.POST:
            r = requests.post(url, data=json.dumps(data), headers=headers)
        elif http_method is Requests.DELETE:
            r = requests.delete(url, headers=headers)
        elif http_method is Requests.PUT:
            r = requests.put(url, data=json.dumps(data), headers=headers)
        elif http_method is Requests.GET:
            r = requests.get(url, headers=headers)
        return r

import pytest

from pmClient.enums import Requests


class Response:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


def test_api_call_helper_200(api_service, mocker):
    params = {
        'access_token': "access_token",
        'public_access_token': "public_access_token",
        'read_access_token': "read_access_token"
    }
    response = Response(200, '{"key": "value"}')
    mocker.patch("pmClient.apiService.ApiService.validate_token", return_value="jwt")
    mocker.patch("pmClient.apiService.ApiService._api_call", return_value=response)
    api_service.api_call_helper('logout', Requests.POST, params, "data")


def test_api_call_helper_200_security_master(api_service, mocker):
    params = {
        'file_name': "security_master"
    }
    response = Response(200, 'text')
    mocker.patch("pmClient.apiService.ApiService.validate_token", return_value="jwt")
    mocker.patch("pmClient.apiService.ApiService._api_call", return_value=response)
    api_service.api_call_helper('security_master', Requests.POST, params, "data")


def test_api_call_helper_400(api_service, mocker):
    params = {
        'access_token': "access_token",
        'public_access_token': "public_access_token",
        'read_access_token': "read_access_token"
    }
    response = Response(400, '{"key": "value"}')
    mocker.patch("pmClient.apiService.ApiService.validate_token", return_value="jwt")
    mocker.patch("pmClient.apiService.ApiService._api_call", return_value=response)
    with pytest.raises(AttributeError):
        api_service.api_call_helper('logout', Requests.POST, params, "data")


def test_api_call_helper_404(api_service, mocker):
    params = {
        'access_token': "access_token",
        'public_access_token': "public_access_token",
        'read_access_token': "read_access_token"
    }
    response = Response(404, '{"key": "value"}')
    mocker.patch("pmClient.apiService.ApiService.validate_token", return_value="jwt")
    mocker.patch("pmClient.apiService.ApiService._api_call", return_value=response)
    with pytest.raises(Exception):
        api_service.api_call_helper('logout', Requests.POST, params, "data")


def test_api_call_helper_415(api_service, mocker):
    params = {
        'access_token': "access_token",
        'public_access_token': "public_access_token",
        'read_access_token': "read_access_token"
    }
    response = Response(415, '{"key": "value"}')
    mocker.patch("pmClient.apiService.ApiService.validate_token", return_value="jwt")
    mocker.patch("pmClient.apiService.ApiService._api_call", return_value=response)
    with pytest.raises(Exception):
        api_service.api_call_helper('logout', Requests.POST, params, "data")


def test_api_call_helper_500(api_service, mocker):
    params = {
        'access_token': "access_token",
        'public_access_token': "public_access_token",
        'read_access_token': "read_access_token"
    }
    response = Response(500, '{"key": "value"}')
    mocker.patch("pmClient.apiService.ApiService.validate_token", return_value="jwt")
    mocker.patch("pmClient.apiService.ApiService._api_call", return_value=response)
    with pytest.raises(Exception):
        api_service.api_call_helper('logout', Requests.POST, params, "data")


def test_api_call_helper_401(api_service, mocker):
    params = {
        'access_token': "access_token",
        'public_access_token': "public_access_token",
        'read_access_token': "read_access_token"
    }
    response = Response(401, '{"key": "value"}')
    mocker.patch("pmClient.apiService.ApiService.validate_token", return_value="jwt")
    mocker.patch("pmClient.apiService.ApiService._api_call", return_value=response)
    with pytest.raises(ConnectionError):
        api_service.api_call_helper('logout', Requests.POST, params, "data")

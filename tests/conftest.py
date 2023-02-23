"""Pytest config"""
from pmClient import PMClient
from pmClient.WebSocketClient import WebSocketClient
from pmClient.apiService import ApiService
import pytest


@pytest.fixture()
def pm_api():
    pm_api = PMClient(api_key="<API_KEY>", api_secret="<API_SECRET>")
    return pm_api


@pytest.fixture()
def web_socket_client():
    web_socket_client = WebSocketClient(public_access_token="<PUBLIC_ACCESS_TOKEN>")
    return web_socket_client


@pytest.fixture()
def api_service():
    api_service = ApiService()
    return api_service

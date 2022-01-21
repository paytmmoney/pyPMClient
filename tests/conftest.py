"""Pytest config"""
from pmClient import PMClient
import pytest


@pytest.fixture()
def pm_api():
    pm_api = PMClient(api_key="<API_KEY>",api_secret="<API_SECRET>")
    return pm_api

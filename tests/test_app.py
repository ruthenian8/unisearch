import pytest
import json
import os
import platform
if platform.system() == "Windows":
    os.system("set TESTING=1")
from unisearch.app import app

@pytest.fixture(scope="module")
def test_client():
    with app.test_client() as testing_client:
        yield testing_client

@pytest.parametrize("arg", [
    "",
    "?=",
    "?=?>+-"
])
def test_search_invalid(test_client, arg):
    response = test_client.get("/" + arg)
    assert response.status_code in [400, 404]

@pytest.parametrize("arg", [
    ""
    "?url="
    "?url=sudo rm -rf ../*",
    "?url=foo bar baz"
])
def test_parse_incorrect(test_client, arg):
    response = test_client.get("/parse" + arg)
    assert response.status_code == 400

@pytest.parametrize("arg", [
    "https://shalamov.ru/library/6/"
])
def test_parse_correct(test_client, arg):
    response = test_client.get("/parse")
    assert response.status_code == 201

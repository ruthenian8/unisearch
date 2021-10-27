import pytest
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
    "?query=лопата",
    "?query=лагерь"
])
def test_search_valid(test_client, arg):
    test_client.get("/parse?url=https://shalamov.ru/library/6/")
    response = test_client.get("/"+arg)
    assert response.status_code == 200
    assert len(response.data) > 0
    assert response.headers["Content-Type"] == "application/json"

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
    "?url=https://shalamov.ru/library/6/"
])
def test_parse_correct(test_client, arg):
    response = test_client.get("/parse")
    assert response.status_code == 201

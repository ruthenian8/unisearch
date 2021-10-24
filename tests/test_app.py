import pytest
import json
from unisearch import app

@pytest.mark.parametrize("input,output", [
    (1,2),
    (3,4)])
def test_one(input, output):
    assert True

@pytest.mark.parametrize("input,output", [
    (1,2),
    (3,4)])
def test_two(input, output):
    assert True

def test_message_form():
    message = "hello world"
    result = app.form_message(message)
    assert type(result) == str
    loaded = json.loads(result)
    assert type(loaded) == dict and "message" in loaded
    assert loaded["message"] == "hello world" 
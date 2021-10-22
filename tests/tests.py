import pytest

@pytest.mark.parametrize("test_one", [(1,2), (3,4)])
def test_one(input, output):
    assert True

@pytest.mark.parametrize("test_two", [(1,2), (3,4)])
def test_two(input, output):
    assert True

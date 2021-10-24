import pytest
from unisearch import utils

@pytest.mark.parametrize("test_input", [
    ("; rm -rf ./*"),
    (";rm-rf./*"),
    (";DROP DATABASE"),
    (";find *passwords* | cat")])
def test_validation(test_input):
    with pytest.raises(AssertionError):
        utils.validate_input(test_input)

@pytest.mark.parametrize("base,link,output", [
    ("https://vk.com", "https://vk.com/feed", "https://vk.com/feed"),
    ("https://vk.com", "/feed", "https://vk.com/feed"),
    ("https://vk.com", None, None),
    ("https://vk.com", "feed", None)])
def test_convert(base, link, output):
    assert utils.convert_relative(link, base) == output

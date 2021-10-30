import tempfile
import pytest
from unisearch import utils
import os


@pytest.mark.parametrize(
    "test_input",
    [("; rm -rf ./*"), (";rm-rf./*"), (";DROP DATABASE"), (";find *passwords* | cat")],
)
def test_validation(test_input):
    with pytest.raises(AssertionError):
        utils.validate_input(test_input)


@pytest.mark.parametrize(
    "base,link,output",
    [
        ("https://vk.com", "https://vk.com/feed", "https://vk.com/feed"),
        ("https://vk.com", "/feed", "https://vk.com/feed"),
        ("https://vk.com", None, None),
        ("https://vk.com", "feed", None),
    ],
)
def test_convert(base, link, output):
    assert utils.convert_relative(link, base) == output


@pytest.mark.asyncio
async def test_read_write(temp_dir):
    filename = os.path.join(temp_dir, "temp")
    await utils.write_file(["hello world"], filename)
    assert os.path.isfile(filename)
    obj = await utils.unpickle(filename)
    assert type(obj) == list
    assert len(obj) == 1
    assert obj[0] == "hello world"

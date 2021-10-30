import pickle
from urllib.parse import urlparse
from typing import Optional, Union
import aiofiles
from lunr.index import Index


async def unpickle(filename: str) -> Union[Index, object]:
    """
    Create a search index from a pickle file
    :param filename: file to read
    """
    async with aiofiles.open(filename, "rb") as file:
        data = await file.read()
        unpacked = pickle.loads(data)
        return unpacked


async def write_file(obj: Union[Index, object], filename: str = "index") -> None:
    """
    Asynchronously pickle an object
    :param obj: object to pickle
    :param filename: name
    """
    async with aiofiles.open(filename, "wb+") as file:
        await file.write(pickle.dumps(obj))


def validate_input(inp: str) -> None:
    """
    assert that the input line is a url and not a command
    :param inp: url from the user
    :raises: AssertionError on incorrect input
    """
    assert " " not in inp and ";" not in inp
    parsed = urlparse(inp)
    assert parsed.scheme != "" and parsed.netloc != ""


def convert_relative(link: str, base: str) -> Optional[str]:
    """
    Build complete links from relative links
    :param link: href to transform
    :param base: base url
    :returns: None if link is cross-resource, otherwise link
    """
    parsed = urlparse(base)
    host = "://".join([parsed.scheme, parsed.netloc])
    if not link:
        return None
    if link.startswith(base) and link != base:
        return link
    if link.startswith("/"):
        return host + link
    return None

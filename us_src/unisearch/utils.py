import pickle
import aiofiles
from lunr.index import Index
from urllib.parse import urlparse
from typing import Optional

async def unpickle(filename:str) -> Index:
    """
    Create a search index from a pickle file
    :param filename: file to read
    """
    async with aiofiles.open(filename, "rb") as f:
        data = await f.read()
        unpacked = pickle.loads(data)
        return unpacked

async def write_file(
    obj:object,
    filename:str="index") -> None:
    """
    Asynchronously pickle an object
    :param obj: object to pickle
    :param filename: name
    """
    async with aiofiles.open(filename, "wb+") as f:
        await f.write(pickle.dumps(obj))

def validate_input(inp:str) -> None:
    assert " " not in inp and ";" not in inp
    parsed = urlparse(inp)
    assert parsed["scheme"] != "" and parsed["netloc"] != ""

def convert_relative(link:str, base:str) -> Optional[str]:
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
    elif link.startswith("/"):
        return host + link
    return None
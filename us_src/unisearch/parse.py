import asyncio
import sys
import chardet
from typing import Dict, List, Optional, Callable
from aiohttp import ClientSession, ClientTimeout
from unisearch.upload import upload
from unisearch.indexing import create_index
from bs4 import BeautifulSoup
from functools import partial
from unisearch.utils import write_file, convert_relative


def detect_encoding(bytes) -> str:
    """
    Get page encoding
    :param bytes: raw server response
    :returns: encoding
    """
    detect = chardet.detect(bytes)
    if detect["encoding"] and detect["confidence"] > 0.7:
        return detect["encoding"]
    return "utf-8"


async def get_page(
        url: str,
        session: ClientSession,
        postprocess: Callable) -> str:
    """
    Get a page with aiohttp, bypassing the decoding problem
    :param url: uri of the page to get
    :returns: decoded page
    """
    try:
        async with session.get(url) as resp:
            data = await resp.read()
            enc = detect_encoding(data)
            data = data.decode(enc)
    except Exception as e:
        print(e)
        return postprocess(url, None)
    return postprocess(url, data)


def extract_links(url: str, text: Optional[str]) -> List[str]:
    """
    Get a list of all links from an index page
    :param url: uri of the page
    :param text: text to parse
    :returns: list of urls
    """
    if text is None:
        return []
    soup = BeautifulSoup(text, "html.parser")
    links = [item.get("href") for item in soup.find_all("a")]
    conversion = partial(convert_relative, base=url)
    return [link for link in map(conversion, links) if link]


def extract_chunks(url: str, text: Optional[str]) -> List[Dict[str, str]]:
    """
    Get all text chunks from a page
    :param url: uri of the page
    :param text: text to parse
    :returns: list dicts {url/text}
    """
    if text is None:
        return []
    soup = BeautifulSoup(text, "html.parser")
    lib_chunks = soup.find_all("dd")  # in case we're parsing lib.ru
    paras = soup.find_all("p")  # for all other purposes
    chunks = [*paras, *lib_chunks]
    return [dict(url=url, text=item.text) for item in chunks]


async def parse(base_uri: str) -> List[Dict[str, str]]:
    """
    Extract indexed pages from a specified resource
    :param base_uri: root for indexed pages
    :returns: Dictionary with id, original uri, and parsed text
    """

    async with ClientSession() as session:
        link_future = asyncio.ensure_future(
            get_page(base_uri, session, extract_links)
        )
        links = await link_future
    if len(links) == 0:
        return []
    async with ClientSession(timeout=ClientTimeout(total=180)) as session:
        tasks = [asyncio.create_task(get_page(link, session, extract_chunks)) for link in links]
        await asyncio.gather(*tasks)
    chunks = []
    for task in tasks:
        if task.done():
            chunks.extend(task.result())
    return [dict(id=str(idx+1), **item) for idx, item in enumerate(chunks)]


async def main(base_uri: str) -> None:
    """
    Parse specified path, save results to DB and create an index file
    :param base_uri: root for indexed pages to parse
    """

    parse_future = asyncio.ensure_future(parse(base_uri))
    result = await parse_future
    index = create_index(result)
    write_task = asyncio.create_task(write_file(index))
    upload(result)
    done, _ = await asyncio.wait({write_task})
    if write_task in done:
        return

if __name__ == "__main__":
    base_uri = sys.argv[1]
    asyncio.run(main(base_uri))
    sys.exit(0)

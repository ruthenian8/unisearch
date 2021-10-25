import asyncio
import pytest
from unisearch import parse
from aiohttp import ClientSession

@pytest.mark.asyncio
async def test_encoding_detection(text_url):
    async with ClientSession() as session:
        async with session.get(text_url) as resp:
            data = await resp.read()
            enc = parse.detect_encoding(data)
            assert type(enc) == str
            assert enc == "utf-8"

@pytest.mark.asyncio
async def test_get_page(text_url, postprocess):
    async with ClientSession() as session:
        result = await parse.get_page(text_url, session, postprocess)
    assert type(result) == str
    assert len(result) > 0

@pytest.mark.asyncio
async def test_parse(link_url):
    result = await parse.parse(link_url)
    assert type(result) == list
    assert len(result) > 0
    assert type(result[0]) == dict
    assert len(result[0]) == 3

def test_link_extraction(link_url, link_page):
    parsed = parse.extract_links(link_url, link_page)
    assert len(parsed) > 0
    assert type(parsed[0]) == str
    assert parsed[0].startswith("http")

def test_text_extraction(text_url, text_page):
    parsed = parse.extract_chunks(text_url, text_page)
    assert len(parsed) > 0
    assert type(parsed[0]) == dict
    assert len(parsed[0]) == 2
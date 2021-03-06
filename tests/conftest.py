import asyncio
import tempfile
import pytest
from aiohttp import ClientSession
from unisearch.parse import get_page


# @pytest.fixture(scope="session")
# def mysql_session():
#     CONFIG["HOST"] = "localhost"
#     db_uri = get_mysql_config()
#     Session = sessionmaker(create_engine(db_uri))
#     with Session() as session:
#         yield session


@pytest.fixture(scope="session")
def temp_dir():
    with tempfile.TemporaryDirectory() as temp:
        yield temp


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def postprocess():
    return lambda x, y: y


@pytest.fixture
def link_url():
    return "https://shalamov.ru/library/6/"


@pytest.fixture
def text_url():
    return "https://shalamov.ru/library/6/2.html"


@pytest.fixture
async def link_page(link_url, postprocess):
    async with ClientSession() as session:
        result = await get_page(link_url, session, postprocess)
    return result


@pytest.fixture
async def text_page(text_url, postprocess):
    async with ClientSession() as session:
        result = await get_page(text_url, session, postprocess)
    return result

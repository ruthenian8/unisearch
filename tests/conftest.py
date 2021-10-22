import pytest
from unisearch.model import db_uri
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine

@pytest.fixture(scope="session")
def mysql_session():
    Session = sessionmaker(create_engine(db_uri))
    with Session() as session:
        yield session
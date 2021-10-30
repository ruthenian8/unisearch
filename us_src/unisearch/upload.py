from typing import List, Dict
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, insert
from sqlalchemy.sql import text as sql_text
from unisearch.model import chunk_table, db_uri


def upload(objects: List[Dict[str, str]]) -> None:
    """
    Upload a list of parsing results to DB
    :param objects: list of dicts {id/url/text}
    """

    engine = create_engine(db_uri)
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    try:
        session.execute(sql_text("""TRUNCATE TABLE {}""".format(chunk_table.name)))
        for obj in objects:
            statement = insert(chunk_table).values(**obj)
            session.execute(statement)
        session.commit()
    except Exception as err:
        session.rollback()
        raise err
    session.close()

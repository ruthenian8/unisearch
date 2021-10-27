from sqlalchemy import MetaData, Column, Integer
from sqlalchemy.dialects.mysql import TINYTEXT, LONGTEXT
from sqlalchemy.schema import Table
from flask_sqlalchemy import SQLAlchemy
from unisearch.config import CONFIG, get_mysql_config
from marshmallow import Schema, fields
import json
import os

db = SQLAlchemy()

if os.environ.get("TESTING", None) == "1":
    CONFIG["HOST"] = "localhost"
db_uri: str = get_mysql_config(**CONFIG)


class Chunks(db.Model):
    """Template for a text paragraph"""
    __tablename__ = CONFIG["tablename"]  # not hardcoding the name of the table
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    url = db.Column("url", TINYTEXT)
    text = db.Column("text", LONGTEXT)

    def __repr__(self):
        return json.dumps(dict(
            id=self.id,
            url=self.url,
            text=self.text
        ))


class ChunkSchema(Schema):
    """Marshmallow class for serializing the server response"""
    id = fields.Int(required=True)
    url = fields.Str(required=True)
    text = fields.Str(required=True)


chunk_schema = ChunkSchema(many=True)

metadata = MetaData()

chunk_table: Table = Table(
    CONFIG["tablename"],  # not hardcoding the name of the table
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("url", TINYTEXT),
    Column("text", LONGTEXT)
)

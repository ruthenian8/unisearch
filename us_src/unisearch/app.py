from typing import Optional, List
import subprocess
import pickle
import re
import json
from flask import Flask, Response, abort, make_response
from flask.globals import request
from lunr.index import Index
from unisearch.model import db, Chunks, db_uri, chunk_schema
from unisearch.utils import validate_input
from unisearch.indexing import construct_query


def create_app() -> Flask:
    """Create a Flask instance"""
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 40 * 1024 * 1024
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_RECORD_QUERIES"] = False
    app.config["SQLALCHEMY_MAX_OVERFLOW"] = 4
    db.app = app
    db.init_app(app)
    db.create_all()
    return app


app = create_app()
lunrindex: Optional[Index] = None


@app.after_request
def after(response: Response) -> Response:
    """Add headers"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["SameSite"] = "Lax"
    response.headers["Content-Type"] = "application/json"
    return response


def form_message(message: str) -> str:
    """
    JSON-encode a message
    :param message: string to encode
    :returns: JSON-string
    """
    return make_response(json.dumps(dict(message=message)))


def process_query(terms: List[str]) -> Response:
    """
    Lookup words in the index, return corresponding paragraphs
    :param terms: list of words to look up
    :returns: flask response
    """
    if len(terms) == 0:
        return form_message("Received an empty query"), 404
    instances = lunrindex.search(construct_query(terms))
    ids = [int(item["ref"]) for item in instances]
    filtered = db.session.query(Chunks).filter(Chunks.id.in_(ids)).all()
    return make_response(chunk_schema.dumps(filtered, many=True))


@app.route("/", methods=["GET"])
def index() -> Response:
    """
    :request.query: word to look up in the index
    :returns: jsonified paragraphs
    """
    if not lunrindex:
        return form_message("Index has not been created yet"), 403
    try:
        query: str = request.args["query"]
    except Exception:
        abort(404)
    terms: List[str] = re.findall(r"\w+", query)
    return process_query(terms)


@app.route("/parse", methods=["GET"])
async def init_parsing() -> Response:
    """
    :request.url: site to parse. See README to view the limitations
    :returns: status 500 if the parsing was successful
    """
    try:
        target: str = request.args["url"]
        validate_input(target)
    except Exception:
        return form_message("Param url missing or invalid"), 400

    returncode = subprocess.run(
        ["python3", "us_src/unisearch/parse.py", target]
    ).returncode
    if returncode == 0:
        global lunrindex
        with open("index", "rb") as file:
            lunrindex = pickle.load(file)
        return form_message("Update successful"), 201
    return form_message("Update failed"), 500


if __name__ == "__main__":
    app.run(debug=False)

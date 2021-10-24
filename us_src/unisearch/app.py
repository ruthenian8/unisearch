import asyncio
import re
import json
from flask import Flask, Response, abort, make_response
from flask.globals import request
from unisearch.model import db, Chunks, db_uri, chunk_schema
from unisearch.utils import unpickle, validate_input
from unisearch.indexing import construct_query
from typing import Optional, List
from lunr.index import Index

def create_app() -> Flask:
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

index:Optional[Index] = None

@app.after_request
def after(response:Response) -> Response:
    response.headers['X-Content-Type-Options'] = "nosniff"
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Cross-Origin-Resource-Policy']='same-origin'
    response.headers['SameSite']='Lax'
    response.headers["Content-Type"] = "application/json"
    return response

def form_message(message:str) -> str:
    return make_response(json.dumps(dict(message=message)))

def process_query(terms:List[str]) -> Response:
    """
    Lookup words in the index, return corresponding paragraphs
    :param terms: list of words to look up
    :returns: flask response
    """
    if len(terms) == 0:
        return Response(
            status=404,
            response=form_message("Received an empty query")
        )
    instances = index.search(construct_query(terms))
    ids = [int(item["id"]) for item in instances]
    filtered = db.session.query(Chunks).filter(Chunks.id.in_(ids)).all()
    return make_response(chunk_schema.dumps(filtered, many=True))

@app.route("/", methods=["GET"])
def index() -> Response:
    """
    :request.query: word to look up in the index
    :returns: jsonified paragraphs
    """
    if not index:
        return Response(
            status=403,
            response=form_message("Index has not been created yet")
        )
    try:
        query:str = request.args["query"]
    except Exception:
        abort(404)
    terms:List[str] = re.findall(r"\w+", query)
    return process_query(terms)
    

@app.route("/parse", methods=["GET"])
async def init_parsing() -> Response:
    """
    :request.url: site to parse. See README to view the limitations
    :returns: status 500 if the parsing was successful
    """
    try:
        target:str = request.args["url"]
        validate_input(target)
    except Exception:
        abort(Response(
            status=400,
            response=form_message("Param url missing or invalid")
        ))
    proc = await asyncio.create_subprocess_shell(
        "python3 indexing.py {}".format(target)
    )
    await proc.wait()
    
    if proc.returncode == 0:
        global index
        index = await unpickle("index")
        return Response(
            status=201,
            response=form_message("Update successful")
        )
    return Response(
        status=500,
        response=form_message("Update failed")
    )
if __name__ == "__main__":
    app.run(debug=True)
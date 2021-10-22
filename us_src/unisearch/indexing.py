from typing import List, Dict
from lunr import get_default_builder, lunr
from lunr.index import Index

def create_index(
    objects: List[Dict[str, str]],
    lang:str="ru") -> Index:
    """
    Produce a lunr search index
    :param objects: list of dicts {id/url/text}
    :param lang: target language
    :returns: a lunr object
    """

    docs: List[Dict[str, str]] = [i for i in map(
        lambda x: dict(id=x["id"], text=x["text"]),
        objects
    )]

    builder = get_default_builder(languages=lang)
    
    idx:Index = lunr(
        ref="id",
        fields=["id", "text"],
        builder=builder,
        documents=docs)

    return idx

def construct_query(terms:List[str]) -> str:
    """
    Redefine the input terms for the search engine
    :param terms: list of words to look up
    :returns: a compliant query
    """
    new_terms = [
        "+text:" + i for i in terms
    ]
    return " ".join(new_terms)
import pytest
from unisearch import indexing
from lunr.index import Index


@pytest.mark.parametrize(
    "inputs,output",
    [(["мама"], "+text:мама"), (["мама", "рама"], "+text:мама +text:рама")],
)
def test_query_construction(inputs, output):
    assert indexing.construct_query(inputs) == output


def test_create_index():
    docs = [
        {"id": 1, "url": "http://ok.ru", "text": "мама мыла раму"},
        {"id": 2, "url": "http://ok.ru", "text": "папа мыл раму"},
    ]
    index = indexing.create_index(docs)
    assert type(index) == Index
    searched = index.search("мама")
    assert len(searched) > 0


def test_create_index_wrong():
    wrong_docs = [
        {"ref": 1, "url": "http://ok.ru", "doc": "мама мыла раму"},
        {"ref": 2, "url": "http://ok.ru", "doc": "папа мыл раму"},
    ]
    with pytest.raises(KeyError):
        indexing.create_index(wrong_docs)

import json

from store import build_index, recall


def test_recall_ranks_relevant_chunk_first():
    chunks = [
        {"path":"a.md","heading":"Benford","text":"benford law digit distribution fraud"},
        {"path":"b.md","heading":"Cats","text":"cats are small animals"},
    ]
    idx = build_index(chunks)
    top = recall(idx, "digit fraud detection", k=1)
    assert top[0]["path"] == "a.md"


def test_recall_orders_multiple_chunks_by_relevance():
    chunks = [
        {"path": "cats.md", "heading": "Cats", "text": "cats are small animals that purr"},
        {"path": "dogs.md", "heading": "Dogs", "text": "dogs are loyal animals that bark"},
        {"path": "fraud.md", "heading": "Fraud", "text": "financial fraud detection using digit analysis and anomaly scoring"},
    ]
    idx = build_index(chunks)
    top = recall(idx, "fraud detection anomaly", k=3)
    assert [r["path"] for r in top][0] == "fraud.md"
    # scores should be non-increasing
    scores = [r["score"] for r in top]
    assert scores == sorted(scores, reverse=True)


def test_recall_with_empty_query_returns_empty_list():
    chunks = [
        {"path": "a.md", "heading": "A", "text": "some text here"},
    ]
    idx = build_index(chunks)
    assert recall(idx, "", k=5) == []
    assert recall(idx, "   ---   ", k=5) == []


def test_recall_with_empty_index_returns_empty_list():
    idx = build_index([])
    assert recall(idx, "anything", k=5) == []


def test_recall_k_larger_than_chunk_count_returns_all_chunks():
    chunks = [
        {"path": "a.md", "heading": "A", "text": "apples and oranges"},
        {"path": "b.md", "heading": "B", "text": "bananas and grapes"},
    ]
    idx = build_index(chunks)
    top = recall(idx, "apples bananas", k=10)
    assert len(top) == 2


def test_index_and_recall_results_are_json_serializable():
    chunks = [
        {"path": "a.md", "heading": "Benford", "text": "benford law digit distribution fraud"},
        {"path": "b.md", "heading": "Cats", "text": "cats are small animals"},
    ]
    idx = build_index(chunks)
    json.dumps(idx)
    json.dumps(recall(idx, "digit fraud", k=2))

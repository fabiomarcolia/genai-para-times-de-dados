from src.retrieval import DocChunk, TfidfRetriever


def test_retrieval_returns_hits():
    chunks = [
        DocChunk(text="receita por mês soma revenue", source_id="1"),
        DocChunk(text="categoria e região", source_id="2"),
    ]
    r = TfidfRetriever(chunks)
    hits = r.search("receita mês", top_k=2)
    assert hits

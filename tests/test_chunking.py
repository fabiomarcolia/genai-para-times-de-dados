from src.chunking import chunk_text


def test_chunk_text_basic():
    text = "a" * 2000
    chunks = chunk_text(text, chunk_size=800, overlap=100)
    assert len(chunks) >= 3
    assert all(len(c) <= 800 for c in chunks[:-1])

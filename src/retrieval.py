from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


@dataclass
class DocChunk:
    text: str
    source_id: str


class TfidfRetriever:
    def __init__(self, chunks: List[DocChunk]):
        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(stop_words=None)
        self.matrix = self.vectorizer.fit_transform([c.text for c in chunks])

    def search(self, query: str, top_k: int = 5) -> List[Tuple[DocChunk, float]]:
        qv = self.vectorizer.transform([query])
        scores = (self.matrix @ qv.T).toarray().ravel()
        idx = np.argsort(scores)[::-1][:top_k]
        return [(self.chunks[i], float(scores[i])) for i in idx if scores[i] > 0]

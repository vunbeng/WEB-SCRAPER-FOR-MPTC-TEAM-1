import re
import asyncio
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 🧠 Load LaBSE once
model = SentenceTransformer("sentence-transformers/LaBSE")

# ✂️ Khmer Chunker (also handles numeric bullets and punctuation)
def chunk_kh(text: str) -> list[str]:
    pattern = r"[។៖,]|[~\-]+|\(\d+\)[\-–]?"
    return [s.strip() for s in re.split(pattern, text) if s.strip()]

# ✂️ English Chunker (also splits by semicolons, parentheses, bullets, conjunctions)
def chunk_en(text: str) -> list[str]:
    pattern = r"[.;:!?]|\(\d+\)|\band\b|\bbut\b|\bor\b"
    return [s.strip() for s in re.split(pattern, text, flags=re.IGNORECASE) if s.strip()]

# 🧬 Embed phrases with LaBSE
async def embed_phrases(phrases: list[str]) -> np.ndarray:
    return model.encode(phrases, normalize_embeddings=True)

# 🔗 Align Khmer & English chunks by cosine similarity
async def align_clauses(kh_text: str, en_text: str, threshold=0.6, top_k=10):
    kh_chunks = chunk_kh(kh_text)
    en_chunks = chunk_en(en_text)

    kh_vecs, en_vecs = await asyncio.gather(
        embed_phrases(kh_chunks),
        embed_phrases(en_chunks)
    )

    scores = cosine_similarity(kh_vecs, en_vecs)
    pairs = []

    for i, row in enumerate(scores):
        j = np.argmax(row)
        score = row[j]
        if score >= threshold:
            pairs.append({
                "khmer": kh_chunks[i],
                "english": en_chunks[j],
                "score": float(score)
            })

    return sorted(pairs, key=lambda x: x["score"], reverse=True)[:top_k]


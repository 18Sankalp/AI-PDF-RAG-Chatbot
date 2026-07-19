import numpy as np
from sentence_transformers import SentenceTransformer


# Load embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Creates embeddings for page-aware chunks.

    Input:
    [
        {
            "text": "chunk content",
            "page": 1
        }
    ]

    Output:
    embeddings as numpy array
    """

    texts = []

    for chunk in chunks:
        texts.append(chunk["text"])

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return np.array(embeddings).astype("float32")


def embed_question(question):
    """
    Creates embedding for user query.
    """

    embedding = model.encode(
        [question]
    )

    return np.array(embedding).astype("float32")
import faiss


def build_index(embeddings):
    """
    Builds FAISS similarity search index.
    """

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index



def search(index, question_embedding, top_k=3):
    """
    Searches most relevant chunks.

    Returns:
    distances and chunk indexes
    """

    distances, indices = index.search(
        question_embedding,
        top_k
    )

    return distances, indices
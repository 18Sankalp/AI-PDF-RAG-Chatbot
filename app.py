from utils.pdf_reader import read_pdf
from utils.chunking import create_chunks
from utils.embedding import create_embeddings
from utils.retrieval import build_index, search
from utils.gemini_helper import ask_gemini

import numpy as np
from sentence_transformers import SentenceTransformer


# Read PDF with page information
pages = read_pdf(
    "data/Advanced Analytics Notes.pdf"
)


# Create page-aware chunks
chunks = create_chunks(pages)


# Create embeddings
embeddings = create_embeddings(chunks)


# Build FAISS index
index = build_index(embeddings)


question = input("Ask your question: ")


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


question_embedding = model.encode(
    [question]
)


question_embedding = np.array(
    question_embedding
).astype("float32")


_, result = search(
    index,
    question_embedding
)


context = "\n\n".join(
    f"Page {chunks[i]['page']}:\n{chunks[i]['text']}"
    for i in result[0]
)


prompt = f"""
You are an expert AI assistant.

Answer ONLY using the provided context.

Always mention the page number when possible.

If the answer is not present, reply:

"I couldn't find that information in the uploaded PDF."


Context:

{context}


Question:

{question}


Answer:
"""


answer = ask_gemini(prompt)


print("\nAI Answer:\n")
print(answer)
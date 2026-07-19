import fitz  # Library to work with PDF files
import os
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)



# Open the PDF
document = fitz.open("data/RNN.pdf")

# Read all text
all_text = ""

for page_number in range(len(document)):
    page = document.load_page(page_number)
    all_text += page.get_text()

document.close()

# Split text into chunks of 500 characters
chunk_size = 500
chunks = []

for i in range(0, len(all_text), chunk_size):
    chunk = all_text[i:i + chunk_size]
    chunks.append(chunk)

print("Total chunks:", len(chunks))
print("\nFirst chunk:\n")
print(chunks[0])

from sentence_transformers import SentenceTransformer

# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings for all chunks
embeddings = model.encode(chunks)

print("Number of embeddings:", len(embeddings))
print("Embedding size:", len(embeddings[0]))

import numpy as np
import faiss

# Convert embeddings to NumPy array
embeddings = np.array(embeddings).astype("float32")

# Create a FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Add embeddings to the index
index.add(embeddings)

print("Vectors stored in FAISS:", index.ntotal)

question = input("Ask your question: ")

question_embedding = model.encode([question])
question_embedding = np.array(question_embedding).astype("float32")

distance, index_result = index.search(question_embedding, k=3)

context = "\n\n".join(
    chunks[i] for i in index_result[0]
)

print("\nRetrieved Context:\n")
print(context)


prompt = f"""
You are an expert AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, reply exactly:

"I couldn't find that information in the uploaded PDF."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents=prompt
)

print("\nAI Answer:\n")
print(response.text)
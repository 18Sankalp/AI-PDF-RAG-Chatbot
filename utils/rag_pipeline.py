from utils.embedding import embed_question
from utils.retrieval import search
from utils.gemini_helper import ask_gemini



def generate_answer(question, index, chunks, history=""):

    # --------------------------------
    # Create question embedding
    # --------------------------------

    question_embedding = embed_question(
        question
    )


    # --------------------------------
    # Search FAISS
    # --------------------------------

    distance, result = search(
        index,
        question_embedding
    )


    # --------------------------------
    # Build context with metadata
    # --------------------------------

    context_parts = []

    sources = []


    for i in result[0]:

        chunk = chunks[i]

        page_number = chunk["page"]

        source_name = chunk.get(
            "source",
            "Uploaded PDF"
        )

        text = chunk["text"]


        context_parts.append(
            f"Source: {source_name}\n"
            f"Page {page_number}:\n"
            f"{text}"
        )


        sources.append(
            {
                "source": source_name,
                "page": page_number
            }
        )


    context = "\n\n".join(
        context_parts
    )


    # Remove duplicate sources

    unique_sources = []

    for source in sources:

        if source not in unique_sources:
            unique_sources.append(source)



    # --------------------------------
    # Gemini Prompt with Memory
    # --------------------------------

    prompt = f"""
You are an expert AI assistant.

Answer the question using ONLY the provided PDF context.

Rules:

1. Use only information from the PDF context.
2. Use conversation history only to understand references.
3. Do not use external knowledge.
4. If information is unavailable, say:

"I couldn't find that information in the uploaded PDF."

5. Provide a clear answer.


Conversation History:

{history}


PDF Context:

{context}


Question:

{question}


Answer:
"""


    # --------------------------------
    # Generate Answer
    # --------------------------------

    answer = ask_gemini(
        prompt,
        context
    )


    # --------------------------------
    # Return for UI
    # --------------------------------

    return answer, unique_sources, context
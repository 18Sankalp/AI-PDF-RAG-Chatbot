from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(pages, chunk_size=500, overlap=100, source="document.pdf"):
    """
    Creates semantic chunks from page-aware PDF text.

    Input:
    pages = [
        {
            "page": 1,
            "text": "page content"
        }
    ]

    Output:
    [
        {
            "text": "chunk content",
            "page": 1,
            "source": "document.pdf"
        }
    ]
    """


    chunks = []


    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )


    for page_data in pages:

        page_number = page_data["page"]

        text = page_data["text"]


        page_chunks = splitter.split_text(text)


        for chunk_text in page_chunks:

            chunks.append(
                {
                    "text": chunk_text,
                    "page": page_number,
                    "source": source
                }
            )


    return chunks
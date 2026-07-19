import fitz


def read_pdf(pdf_source):
    """
    Reads a PDF and returns page-aware text.

    Output:
    [
        {
            "page":1,
            "text":"page content"
        }
    ]
    """

    if isinstance(pdf_source, str):

        document = fitz.open(pdf_source)

    else:

        document = fitz.open(
            stream=pdf_source.read(),
            filetype="pdf"
        )


    pages = []


    for page_number, page in enumerate(document):

        text = page.get_text().strip()

        if text:

            pages.append(
                {
                    "page": page_number + 1,
                    "text": text
                }
            )


    document.close()


    return pages
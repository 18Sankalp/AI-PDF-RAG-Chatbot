import os
from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_gemini(prompt, context=""):

    try:

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text


    except Exception as e:

        error = str(e)

        if "429" in error or "RESOURCE_EXHAUSTED" in error:

            return (
                "⚠️ Gemini API quota exceeded.\n\n"
                "Your PDF retrieval system is working correctly.\n\n"
                "Relevant information retrieved from your document:\n\n"
                f"{context}"
            )

        return (
            "⚠️ Gemini Error occurred.\n\n"
            f"{error}\n\n"
            "Retrieved document information:\n\n"
            f"{context}"
        )
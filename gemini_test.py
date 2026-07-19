import os
from dotenv import load_dotenv
from google import genai

# Load the .env file
load_dotenv()

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Ask Gemini a question
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Explain RNN in one sentence."
)

# Print the answer
print(response.text)
import os
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# List available models
for model in client.models.list():
    print(model.name)
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Read API key from .env
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env")

# Create OpenRouter client
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

try:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": "Say hello to Gayathri and congratulate her for successfully building her AI HRBP Workforce Planner."
            }
        ]
    )

    print("\n========== AI RESPONSE ==========\n")
    print(response.choices[0].message.content)

except Exception as e:
    print("\nERROR:\n")
    print(e)
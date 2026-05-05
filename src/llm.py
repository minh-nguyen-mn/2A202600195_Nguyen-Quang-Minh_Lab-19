from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")


def chat_completion(prompt):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "GraphRAG-Lab"
        }
    )

    return completion.choices[0].message.content
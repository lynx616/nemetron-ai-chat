import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
)

response = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b",
    messages=[
        {
            "role": "user",
            "content": "Explain what Python is in simple terms."
        }
    ],
    temperature=0.7,
    top_p=0.95,
    max_tokens=1000,
    extra_body={
        "chat_template_kwargs": {
            "enable_thinking": True
        }
    },
)

print(response.choices[0].message.content)
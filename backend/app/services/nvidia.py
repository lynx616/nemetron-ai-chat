import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

#  adding the NVIDIA API client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
)


MODEL = "nvidia/nemotron-3-ultra-550b-a55b"


def generate_response(messages):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        top_p=0.95,
        max_tokens=16384,
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": True
            }
        },
    )

    # returning the response
    return response.choices[0].message.content
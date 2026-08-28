from fastapi import APIRouter
from ..schema.chat import ChatRequest
from ..services.nvidia import generate_response


router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):

    messages=[
        {
            "role":"system",
            "content":"you are a helpful AI assistant"
        },
        {
            "role":"user",
            "content":request.message
        }
    ]
    # calling the function from the created nvidia service
    response = generate_response(messages);

    # passing as object that we will get in networks
    return { "response": response }
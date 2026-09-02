from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models.conversation import Conversation
from ..models.message import Message
from ..schema.chat import ChatRequest
from ..services.nvidia import generate_response
from datetime import datetime, timezone


router = APIRouter()


@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    # 1. Find the conversation using the conversation_id from the request
    conversation = db.get(
        Conversation,
        request.conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    # 2. Save the user's message passing into the model
    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )

    db.add(user_message)
    db.commit()

    # 3. Get conversation history of all the messages via Message table 
    history = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation.id
        )
        .order_by(Message.created_at.asc())
        .all()
    )

    # 4. Convert database messages to Nemotron format
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

    for message in history:
        messages.append({
            "role": message.role,
            "content": message.content
        })

    # 5. Generate AI response
    response = generate_response(messages)

    # 6. Save assistant response
    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=response
    )

    db.add(assistant_message)
    db.commit()

    conversation.updated_at = datetime.now(timezone.utc)
    db.commit()
    # 7. Return response
    return {
        "response": response,
        "conversation_id": conversation.id
    }
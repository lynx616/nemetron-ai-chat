from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models.conversation import Conversation
from ..models.message import Message


router = APIRouter()


# Creating a new conversation
@router.post("/conversations")
def create_conversation(
    db: Session = Depends(get_db)
):
    conversation = Conversation(
        title="New Chat"
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return {
        "conversation_id": conversation.id,
        "title": conversation.title
    }


# Get all conversations as objects with their id and title
@router.get("/conversations")
def get_conversations(
    db: Session = Depends(get_db)
):
    conversations = (
        db.query(Conversation)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    return [
        {
            "conversation_id": conversation.id,
            "title": conversation.title
        }
        for conversation in conversations
    ]


# Get all messages from one conversation
@router.get("/conversations/{conversation_id}/messages")
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db)
):
    conversation = db.get(
        Conversation,
        conversation_id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation_id
        )
        .order_by(Message.created_at.asc())
        .all()
    )

    return messages
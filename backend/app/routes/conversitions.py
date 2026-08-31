from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.connection import get_db
from ..models.conversation import Conversation


router = APIRouter()


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
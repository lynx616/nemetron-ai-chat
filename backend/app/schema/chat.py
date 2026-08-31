from pydantic import BaseModel


class ChatRequest(BaseModel):
    # converstiton_id: int because we linking the message table with the conversation table
    conversation_id: int
    message: str
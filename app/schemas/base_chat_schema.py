from typing import Literal
from pydantic import BaseModel

ChatRole = Literal["system", "user", "assistant", "developer"]
class ChatMessage(BaseModel):
    role: ChatRole = "user"
    content: str
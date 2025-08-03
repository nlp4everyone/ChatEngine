from pydantic import BaseModel
from typing import Literal, List, Optional
from .common_schema import *

class ChatMessageInput(BaseModel):
    role: Literal["system", "assistant", "user", "developer"]
    content: str

class ChatCompletionPayload(BaseModel):
    model: str
    messages: List[ChatMessageInput]
    stream: Optional[bool] = False
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None

class ChatCompletionResponse(BaseModel):
    id: str
    object: ResultObject = "chat.completion"
    created: int
    model: str
    choices: List[Choice] = []
    usage: Usage = {}
    service_tier: Optional[str] = ""
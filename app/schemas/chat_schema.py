from typing import Any, Dict
from .common_schema import *
from .base_chat_schema import ChatMessage

class DataItem(ChatMessage):
    id: Optional[str]
    name: Optional[str] = None
    content_parts: Optional[List[str]] = None

class ChatCompletionPayload(BaseModel):
    model: str
    messages: List[ChatMessage]
    stream: Optional[bool] = False
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None

class ChatCompletionResponse(BaseModel):
    id: str
    object: ResultObject = "chat.completion"
    created: int
    model: str
    choices: List[Choice] = None
    usage: Usage = None
    service_tier: Optional[str] = "default"
    system_fingerprint: Optional[str]

class AdvanceChatCompletionResponse(ChatCompletionResponse):
    request_id: Optional[str]
    tool_choice: Any = None
    seed: Optional[int]
    top_p: Optional[float] = 1.0
    temperature: Optional[float] = 1.0
    presence_penalty: Optional[float] = 0.0
    frequency_penalty: Optional[float] = 0.0
    input_user: Optional[Any] = None
    tools: Optional[Any] = None
    metadata: Dict[str, Any] = {}
    response_format: Optional[Any] = None

class ChatMessageResponse(BaseModel):
    object: ResultObject = "list"
    data: List[DataItem]
    first_id: str
    last_id: str
    has_more: bool = False
from typing import List, Optional, Literal
from pydantic import BaseModel
from .base_chat_schema import ChatMessage

ResultObject = Literal["response","chat.completion","list"]


class PromptTokensDetails(BaseModel):
    cached_tokens: int = 0
    audio_tokens: int = 0

class CompletionTokensDetails(BaseModel):
    reasoning_tokens: int = 0
    audio_tokens: int = 0
    accepted_prediction_tokens: int = 0
    rejected_prediction_tokens: int = 0

class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    prompt_tokens_details: PromptTokensDetails = None
    completion_tokens_details: CompletionTokensDetails = None

class ChatCompletionMessageResponse(ChatMessage):
    refusal: Optional[str] = None
    annotations: List = []

class Choice(BaseModel):
    index: int = 0
    message: ChatCompletionMessageResponse
    logprobs: Optional[dict] = None
    finish_reason: Optional[str] = "stop"
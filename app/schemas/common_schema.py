from typing import List, Optional, Literal
from pydantic import BaseModel

ResultObject = Literal["response","chat.completion"]

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
    prompt_tokens_details: PromptTokensDetails
    completion_tokens_details: CompletionTokensDetails

class ChatMessageInputResponse(BaseModel):
    role: Literal["system", "user", "assistant", "developer"] = "user"
    content: str = ""
    refusal: Optional[str] = ""
    annotations: List = []

class Choice(BaseModel):
    index: int = 0
    message: ChatMessageInputResponse
    logprobs: Optional[dict] = {}
    finish_reason: Optional[str] = ""
from fastapi import APIRouter
# Schema
from app.schemas.chat_schema import *
from app.schemas.common_schema import *
# Other component
from app.utils.key_generator import *
from app.utils.token_counter import approximate_count_tokens
# Config
from app.core.config.constants import MODEL_NAME
import time

# Define router
chat_router = APIRouter()

@chat_router.post("/completions")
async def chat_completions(payload: ChatCompletionPayload):
    """
    Creates a model response for the given chat conversation.
    """
    # Pseudo LLM generation
    res = "Hello! How can I help you today?"
    # Define choice
    choice = Choice(index = 0,
                    message = ChatMessageInputResponse(role = "assistant",
                                                       content = res))

    # Define input messages
    input_messages = [message.model_dump() for message in payload.messages]
    # Define token count
    prompt_tokens = approximate_count_tokens(messages = input_messages)
    completion_tokens = approximate_count_tokens(messages = res)
    # Define usage
    usage = Usage(prompt_tokens = prompt_tokens,
                  completion_tokens = completion_tokens,
                  total_tokens = prompt_tokens + completion_tokens,
                  prompt_tokens_details = PromptTokensDetails(),
                  completion_tokens_details = CompletionTokensDetails())

    # Construct output
    return ChatCompletionResponse(id = generate_chat_id(),
                                  created = int(time.time()),
                                  model = MODEL_NAME,
                                  choices = [choice],
                                  system_fingerprint = generate_fingerprint(),
                                  usage = usage)

@chat_router.get("/completions/{completion_id}")
async def get_chat_completions(completion_id: str):
    """
    Get a stored chat completion.
    """
    # Pseudo LLM generation
    input_messages = [ChatMessageInput(role = "user",
                                       content = "Hello").model_dump()]
    res = "Hello! How can I help you today?"

    # Define token count
    prompt_tokens = approximate_count_tokens(messages = input_messages)
    completion_tokens = approximate_count_tokens(messages = res)
    # Define usage
    usage = Usage(prompt_tokens = prompt_tokens,
                  completion_tokens = completion_tokens,
                  total_tokens = prompt_tokens + completion_tokens)
    # Construct output
    return AdvanceChatCompletionResponse(id = completion_id,
                                         created = int(time.time()),
                                         model = MODEL_NAME,
                                         request_id = generate_request_id(),
                                         system_fingerprint = generate_fingerprint(),
                                         seed = generate_seed(),
                                         usage = usage)

@chat_router.get("/completions/{completion_id}/messages")
async def get_chat_messages(completion_id: str):
    """
    Get the messages in a stored chat completion.
    """
    # Pseudo data
    data = [DataItem(id = completion_id,
                     role = "user",
                     content = "Hello")]
    # Construct output
    return ChatMessageResponse(data = data,
                               first_id = completion_id,
                               last_id = completion_id)
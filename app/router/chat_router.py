from fastapi import APIRouter
# Schema
from app.schemas.chat_schema import *
from app.schemas.common_schema import *
from app.schemas.base_chat_schema import ChatMessage
# Other component
from app.utils.key_generator import *
from app.utils.token_counter import approximate_count_tokens
# Config
from app.core.config.constants import *
# LLM
from app.startup import get_model, get_memory_client
# Langchain prompt
from langchain_core.messages import HumanMessage
import time
# Logger
from loggers import SystemLogger

# Define router
chat_router = APIRouter()

@chat_router.post("/completions")
async def chat_completions(payload: ChatCompletionPayload):
    """
    Creates a model response for the given chat conversation.
    """
    llm = get_model()
    memory_client = get_memory_client()
    # Completion id
    completion_id = generate_chat_id()

    # Pseudo LLM generation
    res = await llm.ainvoke([HumanMessage(content = payload.messages[0].content)])
    # Define choice
    choice = Choice(index = 0,
                    message = ChatCompletionMessageResponse(role = "assistant",
                                                            content = res.content))

    # Define input messages
    input_messages = [message.model_dump() for message in payload.messages]
    # Define token count
    prompt_tokens = approximate_count_tokens(messages = input_messages)
    completion_tokens = approximate_count_tokens(messages = res.content)
    # Define usage
    usage = Usage(prompt_tokens = prompt_tokens,
                  completion_tokens = completion_tokens,
                  total_tokens = prompt_tokens + completion_tokens,
                  prompt_tokens_details = PromptTokensDetails(),
                  completion_tokens_details = CompletionTokensDetails())

    # Define session message (For storing)
    session_messages = input_messages.copy()
    session_messages.append(ChatMessage(role = "assistant",
                                        content = res.content).model_dump())
    # Add message to history
    updated_status = await memory_client.add(messages = session_messages,
                            user_id = completion_id,
                            async_mode = True,
                            version="v2")
    # Construct output
    return ChatCompletionResponse(id = completion_id,
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
    input_messages = [ChatMessage(role = "user",
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
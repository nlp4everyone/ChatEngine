from fastapi import FastAPI
# Define startup
from .startup import (init_model,
                      wait_for_vllm,
                      init_memory_client)
# Router
from .router import chat_router
# Components
import time
# Logger
from loggers import SystemLogger
import logging
logging.getLogger("uvicorn.error").propagate = False

# Tags
tags_metadata = [
    {
        "name": "Chat Completion",
        "description": "Contain function including chat completion",
    },
    {
        "name": "Response",
        "description": "Contain features including response",
    }
]
# Define app
app = FastAPI(openapi_tags = tags_metadata)
# Add route
app.include_router(chat_router,
                   prefix = "/v1/chat",
                   tags = [tags_metadata[0].get("name")])

@app.on_event("startup")
async def startup_event():
    # Start
    start = time.perf_counter()
    # Wait until vllm done
    wait_for_vllm()
    # Init ml model
    await init_model()
    # Init memory cline
    init_memory_client()
    end = time.perf_counter()
    SystemLogger.info(f"Start service after :{round(end - start,1)}s")
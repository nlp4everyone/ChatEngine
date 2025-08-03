from fastapi import FastAPI
# Define startup
from .startup import init_model
# Router
from .router import chat_router
# Components
import time

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
    # Init ml model
    # await init_model()
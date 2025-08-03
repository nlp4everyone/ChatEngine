from app.core.config.constants import *
from langchain_openai import ChatOpenAI

async def init_model():
    """Start Postgres Connection"""
    global llm
    llm = ChatOpenAI(model = MODEL_NAME,
                     base_url = "http://localhost:8100/v1",
                     streaming = True,
                     api_key="not-needed-but-required")
    resp = await llm.invoke([("user", "Hello")])
    return llm

def get_model():
    return llm
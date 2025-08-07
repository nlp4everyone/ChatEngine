# Langchain component
from langchain_openai import ChatOpenAI
# Config
from app.core.config.constants import *
# Other component
import requests, time
# Logger
from loggers import SystemLogger

async def init_model(vllm_service_name :str = "vllm",
                     port :int = 8000):
    """Start Postgres Connection"""
    global llm
    llm = ChatOpenAI(model = MODEL_NAME,
                     base_url = f"http://{vllm_service_name}:{port}/v1",
                     streaming = True,
                     api_key = VLLM_API_KEY)

    try:
        resp = await llm.ainvoke("Hello")
        # Response
        SystemLogger.success("Success on sending sample to vLLM")
    except:
        # Response
        SystemLogger.error("Failed to get response from vLLM")
    return llm

def get_model():
    return llm

def wait_for_vllm(vllm_service_name :str = "vllm",
                  vll_port :int = 8000,
                  wait_time :int = 5):
    # Define url
    vllm_url = f"http://{vllm_service_name}:{vll_port}"

    # Loop
    while True:
        # Try to send response
        try:
            response = requests.get(f"{vllm_url}/health")
            if response.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass
        # Wait time
        time.sleep(wait_time)
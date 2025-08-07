import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Model config
MODEL_NAME = os.getenv("MODEL_NAME")
VLLM_API_KEY = os.getenv("VLLM_API_KEY")
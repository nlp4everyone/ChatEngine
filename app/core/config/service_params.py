import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Model config
MEM0_API_KEY = os.getenv("MEM0_API_KEY")
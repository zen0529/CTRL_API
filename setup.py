from os import getenv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from fastapi.security import APIKeyHeader


# Load environment variables
load_dotenv()

PRIMARY_LLM  = ChatOpenAI(
    api_key=getenv("OPENROUTER_API_KEY"),
    base_url=getenv("OPENROUTER_BASE_URL"),
    model="deepseek/deepseek-chat-v3.1:free",
)

FALLBACK_LLM= ChatOpenAI(
  api_key=getenv("OPENROUTER_API_KEY"),
  base_url=getenv("OPENROUTER_BASE_URL"),
  model="openai/gpt-oss-120b:free",
)

# Obtain CTRL API key from .env
CTRL_API_KEY = getenv("CTRL_API_KEY")

# Create API key header dependency
API_KEY_HEADER = APIKeyHeader(name="CTRL_API_KEY", description="API Key needed to access the protected endpoint")
            
from os import getenv
from dotenv import load_dotenv, dotenv_values

load_dotenv()

from langchain_openai import ChatOpenAI
from fastapi.security import APIKeyHeader
from supabase import create_client, Client # type: ignore
import requests


# Load environment variables
# See what dotenv actually loaded
config = dotenv_values(".env")
print("All env variables from .env:")
for key, value in config.items():
    print(f"  {key}: {value[:10] if value else 'None'}...")

# Check if the key exists
api_key = getenv("OPENROUTER_API_KEY")
print(f"\ngetenv result: {repr(api_key)}")

SUPABASE_URL = getenv("SUPABASE_URL")
SUPABASE_KEY = getenv("SUPABASE_API_KEY") #SUPABASE_KEY
SUPABASE: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

api_key=getenv("OPENROUTER_API_KEY")
base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable not set")


print(f"API Key exists: {bool(api_key)}")
print(f"API Key preview: {api_key[:10] if api_key else 'NONE'}...")  # Don't log full keys
print(f"Base URL: {base_url}")
print(f"Loaded key: {repr(api_key)}")

# Raw API test
response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "TestApp"
    },
    json={
        "model": "qwen/qwen3-30b-a3b:free",  # Use a known working model
        "messages": [{"role": "user", "content": "hi"}]
    }
)

print(f"\nStatus Code: {response.status_code}")
print(f"Response: {response.json()}")


SUMMARIZATION_LLM = ChatOpenAI(
    api_key=api_key,
    base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
    # model="deepseek/deepseek-chat-v3.1:free",
    # model="qwen/qwen3-235b-a22b:free"
    # model = "arliai/qwq-32b-arliai-rpr-v1:free"
    model = "z-ai/glm-4.5-air:free"
    # model="google/gemma-3n-e2b-it:free",
    # model="openai/gpt-oss-120b:free"
)

# Initialize Primary LLM
PRIMARY_LLM  = ChatOpenAI(
    api_key=api_key,
    base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
    model = "qwen/qwen3-30b-a3b:free"
)

# Initialize Fallback LLM
FALLBACK_LLM_1= ChatOpenAI(
  api_key=api_key,
  base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
  model="z-ai/glm-4.5-air:free",
)

FALLBACK_LLM_2= ChatOpenAI(
  api_key=api_key,
  base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
  model="minimax/minimax-m2:free",
)


FALLBACK_LLM_3= ChatOpenAI(
  api_key=api_key,
  base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
  model="tngtech/deepseek-r1t2-chimera:free",
)


FALLBACK_LLM_4= ChatOpenAI(
  api_key=api_key,
  base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
  model="deepseek/deepseek-r1-0528-qwen3-8b:free",
)


# Obtain CTRL API key from .env
CTRL_API_KEY = getenv("CTRL_API_KEY")

# Create API key header dependency
API_KEY_HEADER = APIKeyHeader(name="CTRL_API_KEY", description="API Key needed to access the protected endpoint")
            
from os import getenv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from fastapi.security import APIKeyHeader
from sentence_transformers import SentenceTransformer #type: ignore
from langchain_chroma import Chroma # type: ignore


# Load environment variables
load_dotenv()

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize vectordatabase
CHECKINS_DB = Chroma(
    collection_name="user_checkins_db",
    embedding_function=embedding_model,
    persist_directory="./user_db",
)

INSIGHTS_DB = Chroma(
    collection_name="user_insights_db",
    embedding_function=embedding_model,
    persist_directory="./user_db",
)

# Initialize Primary LLM
PRIMARY_LLM  = ChatOpenAI(
    api_key=getenv("OPENROUTER_API_KEY"),
    base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
    model="deepseek/deepseek-chat-v3.1:free",
    # model="google/gemma-3n-e2b-it:free",
    # model="openai/gpt-oss-120b:free"
)

# Initialize Fallback LLM
FALLBACK_LLM= ChatOpenAI(
  api_key=getenv("OPENROUTER_API_KEY"),
  base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
  model="deepseek/deepseek-chat-v3.1:free",
)

# Obtain CTRL API key from .env
CTRL_API_KEY = getenv("CTRL_API_KEY")

# Create API key header dependency
API_KEY_HEADER = APIKeyHeader(name="CTRL_API_KEY", description="API Key needed to access the protected endpoint")
            
from os import getenv
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from fastapi.security import APIKeyHeader
from langchain_chroma import Chroma # type: ignore
from langchain_huggingface import HuggingFaceEmbeddings #type: ignore
from supabase import create_client, Client # type: ignore

model_name = "sentence-transformers/all-MiniLM-L6-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}

SBERT_EMBEDDING = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)


# Load environment variables
load_dotenv()

# Initialize embedding model
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
# embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

SUPABASE_URL = getenv("SUPABASE_URL")
SUPABASE_KEY = getenv("SUPABASE_API_KEY") #SUPABASE_KEY
# SUPABASE = createClient(supabaseUrl, supabaseKey)
SUPABASE: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
# Initialize vectordatabase
CHECKINS_DB = Chroma(
    collection_name="user_checkins_db",
    embedding_function=SBERT_EMBEDDING,
    persist_directory="./user_db",
)

INSIGHTS_DB = Chroma(
    collection_name="user_insights_db",
    embedding_function=SBERT_EMBEDDING,
    persist_directory="./user_db",
)

SUMMARIZATION_LLM = ChatOpenAI(
    api_key=getenv("OPENROUTER_API_KEY"),
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
    api_key=getenv("OPENROUTER_API_KEY"),
    base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
    # model="deepseek/deepseek-chat-v3.1:free",
    model = "qwen/qwen3-30b-a3b:free"
    # model="qwen/qwen3-235b-a22b:free"
    # model = "arliai/qwq-32b-arliai-rpr-v1:free"
    # model = "z-ai/glm-4.5-air:free"
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
            
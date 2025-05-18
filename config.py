import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "openai")
GPT_SIMPLE_MODEL = os.getenv("GPT_SIMPLE_MODEL", "gpt-3.5-turbo")
GPT_CODE_MODEL = os.getenv("GPT_CODE_MODEL", "gpt-4")

QDRANT_HOST = os.getenv("QDRANT_HOST", "http://localhost:6333")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "conversation_memory")

GOOGLE_CALENDAR_CREDENTIALS_PATH = "/Users/satvik/Desktop/AlgorithmX/multi_agent_assistant/credentials.json"  #add your own credentials.json here and also the OAuth Credentials.

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

MEMORY_TOP_K = int(os.getenv("MEMORY_TOP_K", 3)) #for the fetching of 3 latest conversation contexts. 

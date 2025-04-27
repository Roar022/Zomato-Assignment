import os
from dotenv import load_dotenv
from pinecone import Pinecone
from groq import Groq

load_dotenv()

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
LLM = os.getenv("LLM")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

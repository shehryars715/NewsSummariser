import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load API keys from .env
load_dotenv()

# ✅ Create a single embeddings instance
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

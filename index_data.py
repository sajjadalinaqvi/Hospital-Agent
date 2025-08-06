# index_data.py

import os
import uuid
from dotenv import load_dotenv
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Load SentenceTransformer model (384-dim)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX")

# Connect to index
index = pc.Index(index_name)

# Your text data
texts = [
    "Our clinic is open from 9 AM to 6 PM, Monday through Saturday.",
    "Dr. Khan specializes in pediatric care and is available on Tuesdays and Fridays.",
    "You must cancel or reschedule your appointment at least 12 hours in advance.",
    "The clinic accepts all major insurance providers including ABC Health and Medix."
]

# Generate embeddings and upsert
for text in texts:
    embedding = model.encode(text).tolist()
    index.upsert([{
        "id": str(uuid.uuid4()),
        "values": embedding,
        "metadata": {"text": text}
    }])

print("✅ Data uploaded to Pinecone index.")

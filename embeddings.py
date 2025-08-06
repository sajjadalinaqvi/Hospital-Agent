from sentence_transformers import SentenceTransformer
import os
import uuid
from dotenv import load_dotenv
import pinecone

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "clinic-embeddings"

# Connect to Pinecone
pinecone_client = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Check if index exists, else create
if INDEX_NAME not in [index.name for index in pinecone_client.list_indexes()]:
    pinecone_client.create_index(
        name=INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=pinecone.PodSpec(environment="gcp-starter")  # or your specific region/environment
    )

# Connect to the index
index = pinecone_client.Index(INDEX_NAME)

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample texts
texts = [
    "I have a headache and fever",
    "Book an appointment with Dr. Smith",
    "I need a prescription for my cold",
    "My stomach hurts, what should I do?"
]

# Create embeddings and upsert
vectors = []
for text in texts:
    emb = model.encode(text).tolist()
    vectors.append({
        "id": str(uuid.uuid4()),
        "values": emb,
        "metadata": {"text": text}
    })

index.upsert(vectors=vectors)
print("✅ Data embedded and upserted to Pinecone successfully.")

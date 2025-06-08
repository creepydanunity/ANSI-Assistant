from chromadb import Client
from chromadb.config import Settings

client = Client(Settings(persist_directory="chroma_db"))
collection = client.get_collection("code_chunks")

print("✅ Found", collection.count(), "records")

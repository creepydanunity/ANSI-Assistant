from .embedding import process_chunks
from .summarize import enrich_chunks_with_descriptions
from core.config import settings

def process_github(github_url: str, token: str):
    chunks_with_descriptions = enrich_chunks_with_descriptions("https://github.com/creepydanunity/Perceptron", settings.github_token)
    chunks = process_chunks(chunks_with_descriptions)
    
    return chunks
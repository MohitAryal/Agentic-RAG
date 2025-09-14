from sentence_transformers import SentenceTransformer
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
embedding_model = os.getenv("EMBEDDING_MODEL")

model = SentenceTransformer(embedding_model)

async def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    loop = asyncio.get_running_loop()
    embeddings = await loop.run_in_executor(None, model.encode, chunks)
    return embeddings.tolist()
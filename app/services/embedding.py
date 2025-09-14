from sentence_transformers import SentenceTransformer
import asyncio
from dotenv import load_dotenv

load_dotenv()

model = SentenceTransformer(EMBEDDING_MODEL)

async def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    loop = asyncio.get_running_loop()
    embeddings = await loop.run_in_executor(None, model.encode, chunks)
    return embeddings.tolist()
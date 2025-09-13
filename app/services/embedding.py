from sentence_transformers import SentenceTransformer
import asyncio

model = SentenceTransformer("all-MiniLM-L6-v2")

async def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    loop = asyncio.get_running_loop()
    embeddings = await loop.run_in_executor(None, model.encode, chunks)
    return embeddings.tolist()
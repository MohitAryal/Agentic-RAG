from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
import uuid
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
qdrant_url = os.getenv('QDRANT_URL')

qdrant = QdrantClient(url=qdrant_url)

async def save_embeddings_to_vector_db(chunks: list[str], embeddings: list[list[float]], metadata: dict):
    points = []
    for chunk, emb in zip(chunks, embeddings):
        points.append(PointStruct(id=uuid.uuid4().int >> 64, vector=emb, payload={"text": chunk, **metadata}))
    
    qdrant.upsert(collection_name="documents", points=points)
    return [p.id for p in points]

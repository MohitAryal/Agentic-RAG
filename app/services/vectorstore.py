from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import PointStruct, Distance, VectorParams
import uuid
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

qdrant_url = os.getenv('QDRANT_URL')
qdrant_api_key = os.getenv('QDRANT_API_KEY')
vector_size = int(os.getenv('VECTOR_SIZE'))
distance = os.getenv('DISTANCE_METRIC')

DISTANCE_MAP = {
    "cosine": Distance.COSINE,
    "dot": Distance.DOT,
    "euclidean": Distance.EUCLID
}

qdrant = AsyncQdrantClient(url=qdrant_url, api_key=qdrant_api_key)


def get_distance_metric(distance: str, default: str = "cosine") -> Distance:
    selected_metric = distance.lower()
    return DISTANCE_MAP.get(selected_metric, DISTANCE_MAP[default])


async def ensure_collection_exists(user_id: str) -> str:
    collection_name = f"user_{user_id}_documents"
    collections_response = await qdrant.get_collections()
    existing_collections = collections_response.collections

    if not any(c.name == collection_name for c in existing_collections):
        await qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=get_distance_metric(distance)
            )
        )
    return collection_name


async def save_embeddings_to_vector_db(user_id: str, embeddings: list[list[float]], metadata: dict):
    collection = await ensure_collection_exists(user_id)
    
    points = []
    for chunk, emb in zip(chunks, embeddings):
        points.append(PointStruct(id=str(uuid.uuid4()), vector=emb, payload=**metadata))
    
    await qdrant.upsert(collection_name=collection, points=points)
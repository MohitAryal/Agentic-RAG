from app.db.db_session import get_session
from app.db.sqlmodels import FileMetadata
import asyncio

async def save_file_metadata(filename: str, chunking_method: str, chunk_count: int, embedding_model: str):
    async with get_session() as session:
        async with session.begin():
            file_meta = FileMetadata(filename=filename, chunking_method=chunking_method, chunks=chunk_count, used_emb_model=embedding_model)
            session.add(file_meta)
        await session.commit()

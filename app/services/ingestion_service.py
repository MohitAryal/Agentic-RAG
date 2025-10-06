from dotenv import load_dotenv
import os
from services.text_extraction import extract_text_from_file
from services.chunking import chunk_text
from services.embedding import generate_embeddings
from services.vectorstore import save_embeddings_to_vector_db
from services.save_metadata import save_file_metadata

strategy = os.getenv('STRATEGY')
embedding_model = os.getenv('EMBEDDING_MODEL')


async def ingest_file(path, filename):
    # Extract text
    text = await extract_text_from_file(path)
    
    # Chunk text
    chunks = chunk_text(text, strategy=strategy)
    
    # Generate embeddings
    embeddings = await generate_embeddings(chunks)
    
    # Save to vector DB
    await save_embeddings_to_vector_db(chunks=chunks, embeddings=embeddings, metadata={"filename": filename})
    
    # Save metadata to SQL DB
    await save_file_metadata(filename=filename, chunking_method=strategy, chunk_count=len(chunks), embedding_model=embedding_model)
    
    return {"filename": filename, "chunks": len(chunks)}
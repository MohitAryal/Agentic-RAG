from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import aiofiles
from pathlib import Path
from typing import List
from services.text_extraction import extract_text_from_file
from services.chunking import chunk_text
from services.embedding import generate_embeddings
from services.vectorstore import save_embeddings_to_vector_db
from services.save_metadata import save_file_metadata
from dotenv import load_dotenv
import os

router = APIRouter()

load_dotenv()
upload_dir = Path(os.getenv('UPLOAD_DIR'))
strategy = os.getenv('STRATEGY')
embedding_model = os.getenv('EMBEDDING_MODEL')

upload_dir.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    responses = []
    for file in files:
        try:
            # Save file to local storage
            file_path = upload_dir / file.filename
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # Extract text
            text = await extract_text_from_file(file_path)
            
            # Chunk text
            chunks = chunk_text(text, strategy=strategy)
            
            # Generate embeddings
            embeddings = await generate_embeddings(chunks)
            
            # Save to vector DB
            vector_ids = await save_embeddings_to_vector_db(chunks, embeddings, metadata={"filename": file.filename})
            
            # Save metadata to SQL DB
            await save_file_metadata(file.filename, chunking_method=strategy, chunk_count=len(chunks), embedding_model=embedding_model)
            
            responses.append({"filename": file.filename, "chunks": len(chunks), "vector_ids": vector_ids})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return JSONResponse(content={"uploaded_files": responses})

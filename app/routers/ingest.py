from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from services.ingestion_service import ingest_file
import aiofiles
from pathlib import Path
from typing import List
from db.db_session import get_session
from dotenv import load_dotenv
import os

load_dotenv()

upload_dir = Path(os.getenv('UPLOAD_DIR'))
upload_dir.mkdir(exist_ok=True)

router = APIRouter()

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), db: AsyncSession = Depends(get_session)):
    responses = []
    for file in files:
        try:
            # Save file to local storage
            file_path = upload_dir / file.filename
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # Ingest file to vector database
            response = await ingest_file(path=file_path, filename=file.filename)
            responses.append(response)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return JSONResponse(content={"uploaded_files": responses})
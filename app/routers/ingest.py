from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import aiofiles
from pathlib import Path
from typing import List
from db.db_session import get_session
from dependencies import get_user_id
from dotenv import load_dotenv
import os

load_dotenv()

upload_dir = Path(os.getenv('UPLOAD_DIR'))
upload_dir.mkdir(exist_ok=True)

router = APIRouter()

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...), user_id: str = Depends(get_user_id), db: AsyncSession = Depends(get_session)):
    responses = []
    for file in files:
        try:
            # Save file to local storage
            file_path = upload_dir / file.filename
            async with aiofiles.open(file_path, 'wb') as f:
                content = await file.read()
                await f.write(content)
            
            # Ingest file to vector database
            response = ingest_file(path=file_path, filename=file.filename, user_id=user_id)
            responses.append(response)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return JSONResponse(content={"uploaded_files": responses})
from pathlib import Path
from pypdf import PdfReader
import asyncio
import aiofiles

async def extract_text_from_file(file_path: Path) -> str:
    if file_path.suffix.lower() == ".pdf":
        return await extract_text_from_pdf(file_path)

    elif file_path.suffix.lower() == ".txt":
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            text = await f.read()
        return text 

    else:
        raise ValueError("Unsupported file type")

async def extract_text_from_pdf(file_path: Path) -> str:
    reader = PdfReader(file_path)
    num_pages = len(reader.pages)
    text = ''
    for i in range(num_pages):
        page = reader.pages[i]
        text += page.extract_text()
    return text
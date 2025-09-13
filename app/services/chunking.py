from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text: str, strategy: str='fixed', chunk_size: int=1000, chunk_overlap: int=100) -> List[str]:
    if strategy == 'fixed':
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)] 

    elif strategy == 'recursive':
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = splitter.split_text(text)
    
    else:
        raise ValueError('Not a recognized chunking strategy')

    return chunks
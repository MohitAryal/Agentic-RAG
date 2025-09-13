from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ---------- User ----------
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Document ----------
class DocumentBase(BaseModel):
    filename: str
    file_type: str

class DocumentCreate(DocumentBase):
    pass

class DocumentRead(DocumentBase):
    doc_id: int
    user_id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


# ---------- Chunk ----------
class ChunkBase(BaseModel):
    chunk_index: int
    content: str

class ChunkCreate(ChunkBase):
    pass

class ChunkRead(ChunkBase):
    chunk_id: int
    doc_id: int
    embedding_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ---------- Booking ----------
class BookingBase(BaseModel):
    name: str
    email: EmailStr
    scheduled_time: datetime

class BookingCreate(BookingBase):
    pass

class BookingRead(BookingBase):
    booking_id: int
    user_id: Optional[int]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

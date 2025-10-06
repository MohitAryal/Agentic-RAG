from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


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

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str
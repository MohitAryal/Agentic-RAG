from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    userid = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    documents = relationship('Document', back_populates='owner')
    bookings = relationship('Booking', back_populates='user')


class Document(Base):
    __tablename__ = 'document'

    doc_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"))
    filename = Column(String(75), nullable=False)
    filetype = Column(String(15), nullable=False)
    uploaded_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    owner = relationship('User', back_populates='documents')
    chunks = relationship('Chunk', back_populates='document')


class Chunk(Base):
    __tablename__ = "chunk"

    chunk_id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(Integer, ForeignKey("document.doc_id", ondelete="CASCADE"))
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding_id = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="chunks")


class Booking(Base):
    __tablename__ = "booking"

    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="SET NULL"))
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    scheduled_time = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="bookings")
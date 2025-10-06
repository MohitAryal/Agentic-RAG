from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from db.sqlmodels import Base


load_dotenv()
database_url = os.getenv('DATABASE_URL')

# Create async engine
engine = create_async_engine(database_url, echo=True, future=True)

# Create session factory
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency for FastAPI
@asynccontextmanager
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

# Init function to create tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
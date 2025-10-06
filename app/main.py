from fastapi import FastAPI
from routers import ingest
from db.db_session import init_db

app = FastAPI()

# Run once at startup to create tables
@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(ingest.router, tags=["Ingestion"])
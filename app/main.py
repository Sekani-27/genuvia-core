import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.storage import init_schema, save_memory, get_memories

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_schema()
    logger.info("Schema ready")
    yield

app = FastAPI(title="Genuvia Core", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:7007", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MemoryCreate(BaseModel):
    service: str
    type: str
    content: str
    owner: str = "ntando-miya"

@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}

@app.get("/api/memories")
async def list_memories(service: str = None, type: str = None) -> list:
    return await get_memories(service=service, type=type)

@app.post("/api/memories")
async def create_memory(body: MemoryCreate) -> dict:
    return await save_memory(
        service=body.service,
        type=body.type,
        content=body.content,
        owner=body.owner
    )

@app.get("/api/memories/contradictions")
async def list_contradictions() -> list:
    # Basic contradiction detection — same service, similar keywords
    memories = await get_memories()
    flagged = []
    for i, m1 in enumerate(memories):
        for m2 in memories[i+1:]:
            if m1["service"] == m2["service"] and m1["type"] == "decision" and m2["type"] == "decision":
                words1 = set(m1["content"].lower().split())
                words2 = set(m2["content"].lower().split())
                overlap = words1 & words2
                if len(overlap) >= 3:
                    flagged.append({
                        "memory_1": m1,
                        "memory_2": m2,
                        "shared_terms": list(overlap)
                    })
    return flagged

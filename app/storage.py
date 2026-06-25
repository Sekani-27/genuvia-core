import aiosqlite
import uuid
from datetime import datetime, timezone

DB_PATH = "genuvia_core.db"

async def init_schema() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                service TEXT NOT NULL,
                type TEXT NOT NULL CHECK (type IN ('decision', 'commitment', 'lesson')),
                content TEXT NOT NULL,
                owner TEXT NOT NULL DEFAULT 'ntando-miya',
                timestamp TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'active'
            )
        """)
        await db.commit()

async def save_memory(service: str, type: str, content: str, owner: str = "ntando-miya") -> dict:
    memory_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO memories (id, service, type, content, owner, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (memory_id, service, type, content, owner, timestamp)
        )
        await db.commit()
    return {"id": memory_id, "service": service, "type": type, "content": content, "owner": owner, "timestamp": timestamp}

async def get_memories(service: str = None, type: str = None) -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        query = "SELECT * FROM memories WHERE status = 'active'"
        params = []
        if service:
            query += " AND service = ?"
            params.append(service)
        if type:
            query += " AND type = ?"
            params.append(type)
        query += " ORDER BY timestamp DESC"
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

async def close_pool() -> None:
    pass

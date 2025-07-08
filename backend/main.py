from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from fastapi.responses import JSONResponse

app = FastAPI()

class IngestItem(BaseModel):
    source: str
    category: str
    headline: str
    url: str
    timestamp: str  # ISO format

@app.post("/ingest")
async def ingest(items: List[IngestItem]):
    for item in items:
        print(f"[{item.category}] {item.headline} ({item.source})")
        print(f"🔗 {item.url}")
        print(f"🕒 {item.timestamp}")
    return JSONResponse(content={"status": "success", "received": len(items)}) 
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Any
from fastapi.responses import JSONResponse
from fastapi import Body
from backend.summarizer import summarize_batch
from fastapi import Query
from datetime import datetime
from typing import Optional
from fastapi import Form
from fastapi import APIRouter

# In-memory news store: list of dicts with source, category, headline, url, timestamp, summary
news_store = []

app = FastAPI()

class IngestItem(BaseModel):
    source: str
    category: str
    headline: str
    url: str
    timestamp: str  # ISO format
    content: str = None  # Optional full post content

@app.post("/ingest")
async def ingest(payload: Any = Body(...)):
    # Handle possible '=' key wrapping
    items_data = payload.get("=", payload) if isinstance(payload, dict) else payload
    items = [IngestItem(**item) for item in items_data]
    # Use content if available, else headline
    texts_to_summarize = [item.content if item.content else item.headline for item in items]
    summaries = summarize_batch(texts_to_summarize)
    for item, summary in zip(items, summaries):
        print(f"Category: {item.category}")
        print(f"Source: {item.source}")
        print(f"URL: {item.url}")
        print(f"Timestamp: {item.timestamp}")
        print(f"Summary: {summary}\n")
        # Add to in-memory store (no headline, just summary)
        news_store.append({
            "source": item.source,
            "category": item.category,
            "url": item.url,
            "timestamp": item.timestamp,
            "summary": summary
        })
    return JSONResponse(content={
        "status": "success",
        "received": len(items),
        "summaries": summaries
    })

@app.post("/summarize")
async def summarize_news(news_content: str = Form(...)):
    """
    Summarize a long news article or Reddit post into 2-3 factual, plain English lines (no emojis, headlines, or jargon).
    """
    from backend.summarizer import summarize_text
    summary = summarize_text(news_content)
    return {"summary": summary}

@app.get("/digest")
async def digest(category: Optional[str] = Query(None)):
    # Filter by category if provided (case-insensitive, 'All' returns all)
    if category and category.lower() != "all":
        filtered = [item for item in news_store if item["category"].lower() == category.lower()]
    else:
        filtered = news_store
    # Sort by timestamp descending (assume ISO format)
    sorted_items = sorted(filtered, key=lambda x: x["timestamp"], reverse=True)
    # Return up to 5 most recent
    return {"summaries": sorted_items[:5]}

class RedditPost(BaseModel):
    headline: str
    selftext: str
    url: str
    timestamp: str

@app.post("/reddit_summarize")
async def reddit_summarize(posts: List[RedditPost]):
    from backend.summarizer import summarize_batch
    contents = [post.selftext for post in posts]
    summaries = summarize_batch(contents)
    result = []
    for post, summary in zip(posts, summaries):
        result.append({
            "headline": post.headline,
            "summary": summary,
            "url": post.url,
            "timestamp": post.timestamp
        })
    return {"summaries": result} 
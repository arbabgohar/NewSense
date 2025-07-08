# NewSense

## Backend API

### Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the FastAPI server
```bash
uvicorn backend.main:app --reload
```

### /ingest Endpoint
- **POST** `/ingest`
- Accepts: JSON array of objects with fields: `source`, `category`, `headline`, `url`, `timestamp` (ISO string)
- Returns: `{ "status": "success", "received": <number_of_items> }`
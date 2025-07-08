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

## Frontend Dashboard

### Run the Streamlit frontend
```bash
streamlit run frontend/app.py
```

### Features
- Category selection (All, Stock, Cybersecurity, Political, Disaster, Health)
- AI-powered news summarization
- Responsive design for desktop and mobile
- Real-time refresh functionality
- Clean card-based layout

### Usage
1. Start the backend server first
2. Run the Streamlit frontend
3. Select a category and click "Refresh Summaries"
4. View AI-generated summaries in a clean, readable format
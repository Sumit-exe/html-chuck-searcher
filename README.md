HTML Chunk Search with Weaviate

This project allows you to store, search, and display HTML content with similarity scoring using Weaviate for vector search and a React frontend for viewing results.

Features:

* Store HTML chunks with vector embeddings in Weaviate.
* Search content by vector similarity.
* Display results in React with fixed-height cards and View More / View Less toggle.
* Show similarity score for each result.

Tech Stack:

* Backend: Python, FastAPI, Weaviate client
* Vector Database: Weaviate (local or cloud)
* Frontend: React, CSS
* Other: Node.js, npm/yarn

Prerequisites:

* Python >= 3.9
* Node.js >= 14.x
* Weaviate instance (local Docker or cloud)
* pip or poetry for Python packages

Project Setup:

1. Clone the repository

```bash
git clone https://github.com/your-username/html-chunk-search.git
cd html-chunk-search
```

2. Setup Backend
   a) Create Python environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

b) Install dependencies

```bash
pip install -r requirements.txt
```

c) Start Weaviate

```bash
docker run -d \
  -p 8080:8080 \
  -e QUERY_DEFAULTS_LIMIT=20 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true \
  -e PERSISTENCE_DATA_PATH=/var/lib/weaviate \
  -v $(pwd)/weaviate_data:/var/lib/weaviate \
  semitechnologies/weaviate:latest
```

d) Run Backend Server

```bash
uvicorn app.main:app --reload
```

API will run at [http://localhost:8000](http://localhost:8000)

3. Setup Frontend

```bash
cd frontend
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view the React app.

API Endpoints:

* POST /add-document: Add an HTML chunk with embedding to Weaviate.
  Request body example:

```json
{
  "text": "<p>Hello world</p>",
  "embedding": [0.1, 0.2, 0.3, ...]
}
```

* POST /search: Search for HTML chunks by embedding.
  Request body example:

```json
{
  "query_embedding": [0.1, 0.2, 0.3, ...],
  "limit": 10
}
```

Response example:

```json
[
  {
    "html": "<p>Matched HTML chunk</p>",
    "match": 87
  }
]
```

Running the Full Project:

1. Start Weaviate.
2. Start backend server: uvicorn app.main:app --reload
3. Start frontend server: cd frontend && npm start
4. Open [http://localhost:3000](http://localhost:3000) to interact with results.

Project Structure:
html-chunk-search/
├── app/                  # FastAPI backend
│   ├── weaviate_client.py
│   ├── main.py
│   └── ...
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/Results.jsx
│   │   ├── App.jsx
│   │   └── index.js
│   └── package.json
├── requirements.txt
└── README.md

Notes:

* Ensure your Weaviate instance is running before inserting or querying data.
* Backend handles vector embeddings; you can use OpenAI, SentenceTransformers, or any vectorizer.
* Frontend displays results in fixed-height cards with a View More / View Less toggle.

License: MIT License

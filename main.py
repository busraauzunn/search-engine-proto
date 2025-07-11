from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.utils import embedding_functions
import html  # <-- for escaping the output

# Initialize FastAPI
app = FastAPI()

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="documents", embedding_function=embedding_fn)

# Sample documents
SAMPLE_DOCS = [
    {"id": "1", "text": "Company leave policy allows 20 vacation days per year."},
    {"id": "2", "text": "To set up a VPN, follow the steps in the IT handbook."},
    {"id": "3", "text": "Invoices from external partners must be approved by the finance team."},
    {"id": "4", "text": "Employees must complete cybersecurity training annually."},
    {"id": "5", "text": "The sales team uses Salesforce to track client interactions."},
    {"id": "6", "text": "The marketing plan includes social media and email outreach."},
    {"id": "7", "text": "To reset your password, visit the internal IT portal."},
    {"id": "8", "text": "Expense reports must be submitted by the 5th of each month."},
    {"id": "9", "text": "Engineering teams must follow the CI/CD pipeline procedures."},
    {"id": "10", "text": "Remote work guidelines include setting up a secure home network."},
    {"id": "11", "text": "All company devices must have endpoint protection installed."},
    {"id": "12", "text": "Annual performance reviews are scheduled each December."},
    {"id": "13", "text": "Procurement processes require at least 3 vendor quotes."},
    {"id": "14", "text": "Meeting notes should be shared in the Confluence workspace."},
    {"id": "15", "text": "Legal compliance documents are stored in the secure document vault."},
]

# Add sample documents to ChromaDB
for doc in SAMPLE_DOCS:
    try:
        collection.add(documents=[doc["text"]], ids=[doc["id"]])
    except chromadb.errors.IDAlreadyExistsError:
        continue

# HTML Template
HTML_TEMPLATE = """
<html>
<head>
    <title>Document Search</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Poppins', sans-serif;
            background-color: #f4f0ff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .container {{
            background-color: #ffffff;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            text-align: center;
            width: 400px;
        }}
        h2 {{
            color: #6a0dad;
            margin-bottom: 20px;
            font-weight: 500;
            font-size: 20px;
        }}
        form {{
            margin-bottom: 20px;
        }}
        input[type="text"] {{
            padding: 10px;
            width: 80%;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .button-row {{
            display: flex;
            justify-content: center;
            gap: 10px;
        }}
        .btn {{
            padding: 10px 20px;
            background-color: #8b5cf6;
            color: white;
            font-size: 14px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            width: 100px; 
        }}
        .result {{
            background-color: #ede9fe;
            padding: 12px;
            margin-top: 10px;
            border-radius: 8px;
            text-align: left;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2> Internal Document Search</h2>
        <form action="/search" method="get">
            <input type="text" name="query" value="{query}" placeholder="Enter your search..." required autocomplete="off">
            <div class="button-row">
                <button type="submit" class="btn">Search</button>
                <button type="button" class="btn" onclick="window.location.href='/'">Reset</button>
            </div>
        </form>
        {results}
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def home():
    return HTML_TEMPLATE.format(results="", query="")

@app.get("/search", response_class=HTMLResponse)
async def search(query: str = Query(...)):
    results = collection.query(query_texts=[query], n_results=2)

    if not results.get("documents") or not results["documents"][0]:
        items = "<div class='result'>No results found.</div>"
    else:
        items = ""
        for doc in results.get("documents", [[]])[0]:
            safe_text = html.escape(doc)  # <-- escaping to prevent HTML injection
            items += f"<div class='result'>{safe_text}</div>"

    return HTML_TEMPLATE.format(results=items, query=html.escape(query))

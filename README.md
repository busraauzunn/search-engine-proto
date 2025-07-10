# search-engine-proto

# Internal Document Search - Prototype

This repository contains a prototype for an internal document search engine.  
It demonstrates how employees can search company documents using natural language queries, supported by semantic search.

## Features
- FastAPI web server with a basic HTML interface
- AI-powered semantic search using Sentence Transformers
- ChromaDB vector database for storing and searching document embeddings
- Example dataset with sample company documents

## Technology Stack
- Python 3.13
- FastAPI
- ChromaDB
- Sentence Transformers (MiniLM-L6-v2)
- HTML/CSS (basic)

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/search-prototype.git
   cd search-prototype

2. Create and activate a virtual environment:

```bash
python -m venv venv
.\venv\Scripts\Activate

3. Install dependencies:

pip install -r requirements.txt


4. Start the server:

```bash
uvicorn main:app --reload

5.Access the app in your browser at:

```bash
http://127.0.0.1:8000


Example Search Queries
vpn
vacation days
reset password
invoices
cybersecurity training

Next Steps (Suggested Improvements)
Add real document parsing (PDF, Word, emails)
Implement user authentication and permissions
Improve frontend with a modern framework
Scale with a production-grade vector database


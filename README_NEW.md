# SimpleRAG_langChain

A simple Retrieval-Augmented Generation (RAG) project using **LangChain**, **FastAPI**, and **Streamlit**.

**🆕 NEW: Blog Chat Integration** - Now integrated with Hugo blog for automated Q&A! See [BLOG_RAG_DEPLOYMENT.md](BLOG_RAG_DEPLOYMENT.md) for details.

---

## 🚀 Quick Start (Blog Integration)

### Option 1: Automatic Setup
```bash
# Windows
start.bat

# This will:
# 1. Install dependencies
# 2. Embed blog posts into vector DB
# 3. Run tests
# 4. Start API server
```

### Option 2: Manual Setup

**1. Install dependencies:**
```bash
pip install -r requirements.txt
```

**2. Embed blog posts:**
```bash
python embed_blog_posts.py
```

**3. Start API server:**
```bash
uvicorn api.app:app --reload --port 8000
```

**4. Start Hugo blog (in separate terminal):**
```bash
cd C:\Code\DA_NetworkingPrograming\NetworkingPrograming
hugo server -D
```

**5. Open browser:**
- Blog: http://localhost:1313/NetworkingPrograming/blogs/
- API Docs: http://localhost:8000/docs

---

## 🎯 Features

### Blog Chat Assistant
- ✅ Intelligent Q&A for blog content
- ✅ Source citations with links
- ✅ Multilingual support (Vietnamese/English)
- ✅ Real-time responses
- ✅ Embedded in blog pages

### RAG System
- ✅ Vector-based document retrieval
- ✅ Semantic search using HuggingFace embeddings
- ✅ FastAPI backend with CORS support
- ✅ Streamlit UI for testing

---

## 📂 Project Structure
```
SimpleRAG_langChain/
├── api/                         # FastAPI backend
│   └── app.py                   # API endpoints including /chat
├── data/                        # Your documents (PDFs, etc.)
├── src/                         # Core logic
│   ├── loader.py                # PDF document loader
│   ├── markdown_loader.py       # 🆕 Hugo markdown loader
│   ├── embedded_store.py        # Vector database management
│   └── retriever.py             # Retrieval logic
├── ui/                          # Streamlit UI
│   ├── streamlit_app.py
│   └── graph.py
├── vectorstore/                 # ChromaDB storage
├── embed_blog_posts.py          # 🆕 Blog embedding script
├── test_system.py               # 🆕 Integration tests
├── start.bat                    # 🆕 Quick start script (Windows)
├── ingest.py                    # Document ingestion for PDFs
├── requirements.txt             # Dependencies
├── README.md                    # This file
└── BLOG_RAG_DEPLOYMENT.md       # 🆕 Detailed deployment guide
```

---

## 📖 Original Workflow (PDF Documents)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your documents
Place your PDF or text files into the `/data/` folder.

### 3. Update ingest pipeline
Edit `ingest.py` and add the file paths of the documents you want to include in the vector store.

### 4. Run the ingestion
```bash
python ingest.py
```

### 5. Start the API server
```bash
uvicorn api.app:app --reload --port 8000
```

API will be available at: [http://localhost:8000](http://localhost:8000)

### 6. Launch the Streamlit UI
```bash
streamlit run ui/streamlit_app.py
```

UI will be available at: [http://localhost:8501](http://localhost:8501)

---

## 🔌 API Endpoints

### POST /chat
Chat endpoint for blog assistant (Blog Integration)

**Request:**
```json
{
  "question": "TCP 3-way handshake là gì?",
  "k": 3
}
```

**Response:**
```json
{
  "question": "TCP 3-way handshake là gì?",
  "answer": "...",
  "sources": [
    {
      "title": "Java Socket: Cơ bản",
      "url": "/blogs/java-socket-co-ban/",
      "excerpt": "...",
      "filename": "java-socket-co-ban.md"
    }
  ],
  "total_sources": 3
}
```

### GET /query_chunks
Query by chunks (fine-grained retrieval)

### GET /query_documents
Query by documents (document-level retrieval)

### GET /query_both
Combined document and chunk retrieval

### POST /graph
Generate topic-document graph

### GET /list_documents
List all documents in vectorstore

### GET /health
Health check endpoint

---

## 🧪 Testing

Run integration tests:
```bash
python test_system.py
```

This will test:
- Health check endpoint
- Vector database status
- Query chunks retrieval
- Chat endpoint functionality

---

## 📚 Documentation

- **[BLOG_RAG_DEPLOYMENT.md](BLOG_RAG_DEPLOYMENT.md)** - Complete deployment guide for blog integration
- **API Documentation** - Available at http://localhost:8000/docs when server is running

---

## 🛠️ Technologies Used

- **LangChain** - RAG framework
- **FastAPI** - Web API framework
- **ChromaDB** - Vector database
- **HuggingFace** - Embeddings (sentence-transformers)
- **Streamlit** - Interactive UI
- **Hugo** - Static site generator (for blog)

---

## 🎓 Use Cases

1. **Blog Q&A System** - Users can ask questions about blog content
2. **Research Paper Analysis** - Query and analyze academic papers
3. **Document Search** - Semantic search across documents
4. **Knowledge Base** - Build an interactive knowledge base

---

## 📝 License

This project is for educational purposes.

# SimpleRAG_langChain

A simple Retrieval-Augmented Generation (RAG) project using **LangChain**, **FastAPI**, and **Streamlit**.

---

## 🚀 Getting Started

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

## 📂 Project Structure
```
SimpleRAG_langChain/
├── api/                # FastAPI backend
├── data/               # Your documents (PDFs, etc.)
├── lib/                # External libraries
├── src/                # Core logic (loader, retriever, vector store)
├── ui/                 # Streamlit UI
├── ingest.py           # Document ingestion script
├── requirements.txt    # Dependencies
└── README.md
```

---

## ✨ Features
- **FastAPI** for serving the RAG API
- **Streamlit** for a simple web-based UI
- **LangChain** for retrieval and document processing
- Easy document ingestion pipeline

---

## 📝 Notes
- Always re-run `ingest.py` after adding new documents.
- Make sure the API is running before launching the Streamlit UI.

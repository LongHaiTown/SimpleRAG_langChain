from typing import List
from fastapi import FastAPI, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from src.embedded_store import load_vector_db
from src.retriever import build_topic_doc_graph, retrieve_chunks, retrieve_documents, query_both_levels

app = FastAPI(title="RAG Blog Assistant API")

# CORS middleware để cho phép frontend truy cập
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên chỉ định domain cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load vector DB khi server start
vectordb = load_vector_db()


@app.get("/query_chunks")
def query_chunks_api(q: str = Query(...), k: int = 3):
    """Truy vấn theo chunk."""
    docs = retrieve_chunks(vectordb, q, k)
    return {
        "query": q,
        "chunks": [
            {
                "chunk_id": i,
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
            for i, doc in enumerate(docs, start=1)
        ]
    }

@app.get("/query_documents")
def query_documents_api(q: str = Query(...), k: int = 2, chunk_k: int = 5):
    """Truy vấn theo document."""
    ranked_docs = retrieve_documents(vectordb, q, k=k, chunk_k=chunk_k)
    return {
        "query": q,
        "documents": [
            {"doc_source": doc, "score": score}
            for doc, score in ranked_docs
        ]
    }


@app.get("/query_both")
def query_both_api(q: str = Query(...), k_doc: int = 2, k_chunk: int = 3):
    """Truy vấn cả document-level và chunk-level."""
    results = query_both_levels(vectordb, q, k_doc, k_chunk)
    
    chunk_json = [
        {
            "chunk_id": i,
            "content": doc.page_content,
            "metadata": doc.metadata,
        }
        for i, doc in enumerate(results["chunks"], start=1)
    ]
    return {
        "query": q,
        "documents": results["documents"],
        "chunks": chunk_json
    }


@app.get("/list_documents")
def list_documents():
    """Lấy danh sách tất cả tài liệu trong vectorstore."""
    collection = vectordb._collection.get(include=["metadatas"])
    metadatas = collection["metadatas"]

    docs = {}
    for meta in metadatas:
        if meta and "doc_id" in meta:
            docs[meta["doc_id"]] = meta.get("source_file", "unknown")

    results = [{"doc_id": k, "source_file": v} for k, v in docs.items()]
    return {"documents": results}


@app.post("/graph")
def graph_api(
    topics: List[str] = Body(..., example=["RAG", "Cryptanalysis", "Consensus Algorithm"]),
    top_k: int = Query(5, description="Số documents mỗi topic")
):
    """
    Sinh graph topic ↔ document.
    - Input: danh sách chủ đề (topics)
    - Output: JSON gồm nodes và edges
    """
    graph = build_topic_doc_graph(vectordb, topics, top_k=top_k)
    return graph


@app.post("/chat")
def chat_api(
    question: str = Body(..., embed=True),
    k: int = Body(3, embed=True)
):
    """
    Chat endpoint cho blog assistant.
    Trả về câu trả lời và các nguồn tham khảo.
    
    Args:
        question: Câu hỏi của người dùng
        k: Số lượng chunks để retrieve (default: 3)
    
    Returns:
        {
            "question": str,
            "answer": str,
            "sources": [{"title": str, "url": str, "excerpt": str}]
        }
    """
    # Retrieve relevant chunks
    docs = retrieve_chunks(vectordb, question, k=k)
    
    # Build context from retrieved chunks
    context_parts = []
    sources = []
    
    for i, doc in enumerate(docs, start=1):
        # Add to context
        context_parts.append(f"[Nguồn {i}]\n{doc.page_content}\n")
        
        # Build source info
        metadata = doc.metadata
        title = metadata.get('title', 'Untitled')
        filename = metadata.get('filename', '')
        
        # Create URL (assuming blog structure)
        # Ví dụ: java-socket-co-ban.md -> /blogs/java-socket-co-ban/
        blog_slug = filename.replace('.md', '') if filename else ''
        url = f"/blogs/{blog_slug}/" if blog_slug else "#"
        
        # Get excerpt (first 200 chars)
        excerpt = doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
        
        sources.append({
            "title": title,
            "url": url,
            "excerpt": excerpt,
            "filename": filename
        })
    
    # Combine context
    full_context = "\n".join(context_parts)
    
    # Generate answer (simple concatenation for now)
    # TODO: Integrate with LLM for better answers
    answer = f"Dựa trên các bài viết trong blog, đây là những thông tin liên quan đến câu hỏi của bạn:\n\n{full_context}"
    
    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "total_sources": len(sources)
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "RAG Blog Assistant API is running"}
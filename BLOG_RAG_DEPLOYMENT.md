# 🤖 Hướng dẫn Triển khai Hệ thống RAG Chat cho Blog

## Tổng quan

Hệ thống này kết nối giao diện chat trên website blog (DA_NetworkingPrograming) với backend RAG (SimpleRAG_langChain) để người dùng có thể đặt câu hỏi về nội dung các bài blog và nhận câu trả lời tự động.

## Kiến trúc Hệ thống

```
┌─────────────────────────────────────────┐
│   Frontend (Hugo Blog)                  │
│   - Chat Widget (JavaScript)            │
│   - User Interface                      │
└──────────────┬──────────────────────────┘
               │ HTTP POST
               │ /chat
               ▼
┌─────────────────────────────────────────┐
│   Backend API (FastAPI)                 │
│   - /chat endpoint                      │
│   - CORS enabled                        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│   RAG System                            │
│   - Vector DB (Chroma)                  │
│   - HuggingFace Embeddings              │
│   - Retriever                           │
└─────────────────────────────────────────┘
```

## Các File Đã Tạo/Cập Nhật

### 1. Backend RAG System (SimpleRAG_langChain)

#### Mới tạo:
- `src/markdown_loader.py` - Loader cho Hugo markdown files
- `embed_blog_posts.py` - Script embedding toàn bộ blogs

#### Đã cập nhật:
- `api/app.py` - Thêm CORS và endpoint `/chat`

### 2. Frontend (DA_NetworkingPrograming)

#### Đã cập nhật:
- `static/js/chat-widget.js` - Cấu hình API endpoint mới
- `public/js/chat-widget.js` - Đồng bộ với static

## Hướng dẫn Triển khai

### Bước 1: Cài đặt Dependencies

```bash
cd C:\Code\DACN_MindMapNote\SimpleRAG_langChain
pip install -r requirements.txt
```

Đảm bảo `requirements.txt` có các packages:
- langchain
- langchain-community
- langchain-huggingface
- fastapi
- uvicorn
- chromadb
- sentence-transformers

### Bước 2: Embedding Blog Posts

Chạy script để embedding toàn bộ blog posts vào vector database:

```bash
cd C:\Code\DACN_MindMapNote\SimpleRAG_langChain
python embed_blog_posts.py
```

**Output mong đợi:**
```
🚀 Starting blog embedding process...
📂 Blog directory: c:/Code/DA_NetworkingPrograming/NetworkingPrograming/content/blogs
💾 Vector store directory: vectorstore
------------------------------------------------------------

📖 Loading and splitting blog posts...
✅ Loaded 12 blog posts from c:/Code/DA_NetworkingPrograming/NetworkingPrograming/content/blogs
✅ Split into 156 chunks

🔖 Generated doc_id: a1b2c3d4e5f6...

💿 Creating/updating vector database...
   Total chunks to embed: 156
✅ Upserted 156 chunks for doc blogs_collection_...

============================================================
✅ Blog embedding completed successfully!
============================================================

📊 Summary:
   - Total blog posts processed: 12
   - Total chunks created: 156
   - Doc ID: a1b2c3d4e5f6...
   - Vector store location: vectorstore

🧪 Testing retrieval...
   Query: 'TCP socket'
   Found 3 results:
      1. Java Socket: Cơ bản
      2. TCP vs UDP
      3. Multi-threading Socket
```

### Bước 3: Khởi động API Server

```bash
cd C:\Code\DACN_MindMapNote\SimpleRAG_langChain
uvicorn api.app:app --reload --port 8000
```

**Kiểm tra API:**
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs

### Bước 4: Kiểm tra Chat Interface

1. Khởi động Hugo server:
```bash
cd C:\Code\DA_NetworkingPrograming\NetworkingPrograming
hugo server -D
```

2. Truy cập: http://localhost:1313/NetworkingPrograming/blogs/

3. Test chat widget:
   - Nhấn vào icon chat ở góc dưới phải
   - Thử các câu hỏi mẫu
   - Hoặc gõ câu hỏi của bạn

## API Endpoints

### POST /chat

Request:
```json
{
  "question": "TCP 3-way handshake là gì?",
  "k": 3
}
```

Response:
```json
{
  "question": "TCP 3-way handshake là gì?",
  "answer": "Dựa trên các bài viết trong blog...",
  "sources": [
    {
      "title": "Java Socket: Cơ bản",
      "url": "/blogs/java-socket-co-ban/",
      "excerpt": "TCP 3-way handshake là quá trình...",
      "filename": "java-socket-co-ban.md"
    }
  ],
  "total_sources": 3
}
```

### GET /health

Response:
```json
{
  "status": "healthy",
  "message": "RAG Blog Assistant API is running"
}
```

## Cấu hình

### Frontend (chat-widget.js)

```javascript
const CONFIG = {
    API_ENDPOINT: 'http://localhost:8000/chat',
    USE_MOCK: false,  // false = dùng API thật, true = mock demo
    MAX_SOURCES: 3    // Số lượng nguồn tham khảo
};
```

### Backend (embed_blog_posts.py)

```python
BLOG_DIR = "c:/Code/DA_NetworkingPrograming/NetworkingPrograming/content/blogs"
```

## Cải tiến Nâng cao (Optional)

### 1. Tích hợp LLM để sinh câu trả lời tốt hơn

Hiện tại API đang trả về context trực tiếp. Để cải thiện:

```python
# Trong api/app.py, thêm vào endpoint /chat
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

llm = OpenAI(temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectordb.as_retriever(search_kwargs={"k": k})
)

answer = qa_chain.run(question)
```

### 2. Caching kết quả

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_response(question: str):
    # ... retrieval logic
    pass
```

### 3. Logging và Monitoring

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/chat")
def chat_api(...):
    logger.info(f"Question received: {question}")
    # ...
```

## Xử lý Lỗi Thường Gặp

### Lỗi: "Connection refused" khi gọi API

**Nguyên nhân:** API server chưa chạy

**Giải pháp:** 
```bash
uvicorn api.app:app --reload --port 8000
```

### Lỗi: "No module named 'langchain'"

**Nguyên nhân:** Chưa cài đặt dependencies

**Giải pháp:**
```bash
pip install -r requirements.txt
```

### Lỗi: "Vector store not found"

**Nguyên nhân:** Chưa chạy embedding script

**Giải pháp:**
```bash
python embed_blog_posts.py
```

### Lỗi: CORS policy

**Nguyên nhân:** Frontend và backend khác origin

**Giải pháp:** Đã được xử lý trong `api/app.py` với CORSMiddleware

## Demo cho Giảng viên

### Script Demo:

1. **Giới thiệu hệ thống:**
   "Thưa thầy/cô, em xin demo hệ thống RAG Chat Assistant đã được tích hợp vào blog."

2. **Mở trang blog:**
   "Đây là trang blog của em với các bài viết về Network Programming."

3. **Mở chat widget:**
   "Em đã tích hợp một chat assistant ở đây (click icon). Người dùng có thể hỏi bất kỳ câu hỏi nào về nội dung blog."

4. **Demo câu hỏi:**
   - "TCP 3-way handshake là gì?"
   - "Sự khác biệt giữa TCP và UDP?"
   - "Code mẫu Java Socket Server?"

5. **Giải thích kỹ thuật:**
   "Hệ thống sử dụng RAG (Retrieval-Augmented Generation):
   - Embedding toàn bộ blog posts vào vector database
   - Khi người dùng hỏi, hệ thống tìm kiếm các đoạn văn liên quan
   - Trả về câu trả lời kèm nguồn tham khảo"

6. **Show backend:**
   "Backend được xây dựng bằng FastAPI, sử dụng LangChain và ChromaDB. (Mở API docs tại localhost:8000/docs)"

## Kết luận

Hệ thống đã được hoàn thiện với:
- ✅ Giao diện chat tích hợp vào blog
- ✅ Backend RAG với FastAPI
- ✅ Embedding toàn bộ blog posts
- ✅ API endpoint /chat hoàn chỉnh
- ✅ CORS đã được cấu hình
- ✅ Trả về nguồn tham khảo (sources)

Người dùng có thể hỏi bất kỳ câu hỏi nào về nội dung blog và nhận được câu trả lời tự động cùng với các nguồn tham khảo.

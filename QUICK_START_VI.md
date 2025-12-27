# 🚀 Hướng dẫn Nhanh - RAG Blog Chat

## Tổng quan
Hệ thống cho phép người dùng đặt câu hỏi về nội dung blog và nhận câu trả lời tự động từ AI.

## Cách chạy (3 bước)

### Bước 1: Cài đặt và Embedding

Mở PowerShell/CMD tại thư mục `SimpleRAG_langChain`:

```bash
# Cài đặt dependencies (chỉ cần làm 1 lần)
pip install -r requirements.txt

# Embedding toàn bộ blog posts
python embed_blog_posts.py
```

**Kết quả mong đợi:**
```
🚀 Starting blog embedding process...
✅ Loaded 12 blog posts
✅ Split into 156 chunks
✅ Blog embedding completed successfully!
```

### Bước 2: Khởi động API Server

```bash
uvicorn api.app:app --reload --port 8000
```

**Kiểm tra:** Mở http://localhost:8000/docs để xem API documentation

### Bước 3: Khởi động Hugo Blog

Mở terminal mới tại thư mục `NetworkingPrograming`:

```bash
hugo server -D
```

**Kiểm tra:** Mở http://localhost:1313/NetworkingPrograming/blogs/

## Test Chat Widget

1. Truy cập trang blog: http://localhost:1313/NetworkingPrograming/blogs/
2. Nhấn vào icon chat ở góc dưới phải (💬)
3. Thử các câu hỏi:
   - "TCP 3-way handshake là gì?"
   - "Sự khác biệt giữa TCP và UDP"
   - "Code mẫu Java Socket Server"

## Cách chạy nhanh hơn

**Windows:** Double-click file `start.bat` trong thư mục SimpleRAG_langChain

Script này sẽ tự động:
1. ✅ Kiểm tra dependencies
2. ✅ Chạy embedding (nếu cần)
3. ✅ Test hệ thống
4. ✅ Khởi động API server

## Giải thích các file chính

### Backend (SimpleRAG_langChain)

- `embed_blog_posts.py` - Script embedding blogs vào vector DB
- `src/markdown_loader.py` - Đọc và xử lý markdown files
- `api/app.py` - API server với endpoint `/chat`
- `test_system.py` - Script test tự động
- `start.bat` - Script khởi động nhanh

### Frontend (NetworkingPrograming)

- `static/js/chat-widget.js` - Code JavaScript cho chat widget
- `static/css/chat-widget.css` - Style cho chat widget
- `layouts/partials/blog-chat.html` - HTML template

## Cấu trúc API

### POST /chat

**Request:**
```json
{
  "question": "TCP là gì?",
  "k": 3
}
```

**Response:**
```json
{
  "answer": "TCP (Transmission Control Protocol)...",
  "sources": [
    {
      "title": "Java Socket: Cơ bản",
      "url": "/blogs/java-socket-co-ban/",
      "excerpt": "..."
    }
  ]
}
```

## Troubleshooting

### Lỗi: "Connection refused"
**Nguyên nhân:** API server chưa chạy  
**Giải pháp:** `uvicorn api.app:app --reload --port 8000`

### Lỗi: "No module named 'langchain'"
**Nguyên nhân:** Chưa cài dependencies  
**Giải pháp:** `pip install -r requirements.txt`

### Lỗi: "Vector store not found"
**Nguyên nhân:** Chưa chạy embedding  
**Giải pháp:** `python embed_blog_posts.py`

### Chat không hoạt động
1. Kiểm tra API server đang chạy: http://localhost:8000/health
2. Kiểm tra console trong browser (F12)
3. Kiểm tra cấu hình trong `chat-widget.js`:
   ```javascript
   const CONFIG = {
       API_ENDPOINT: 'http://localhost:8000/chat',
       USE_MOCK: false  // Phải là false
   };
   ```

## Demo cho giảng viên

### Script demo:

**1. Giới thiệu:**
> "Thưa thầy/cô, em đã xây dựng hệ thống RAG để trả lời tự động các câu hỏi về nội dung blog."

**2. Show architecture:**
> "Hệ thống gồm 3 phần:
> - Frontend: Chat widget tích hợp vào Hugo blog
> - Backend: FastAPI với LangChain
> - Database: ChromaDB vector store"

**3. Demo live:**
> "Em xin demo trực tiếp trên blog..."
> [Click chat icon, gõ câu hỏi]

**4. Giải thích kỹ thuật:**
> "Khi người dùng hỏi, hệ thống:
> 1. Embedding câu hỏi thành vector
> 2. Tìm kiếm semantic trong vector DB
> 3. Lấy ra các đoạn văn liên quan nhất
> 4. Trả về câu trả lời kèm nguồn tham khảo"

**5. Show code (nếu được hỏi):**
- API endpoint: `api/app.py` - hàm `chat_api()`
- Markdown loader: `src/markdown_loader.py`
- Frontend: `static/js/chat-widget.js`

## Tính năng nổi bật

✅ **Tự động:** Embedding toàn bộ blog posts  
✅ **Thông minh:** Semantic search, không chỉ keyword matching  
✅ **Trích nguồn:** Mỗi câu trả lời đều có link đến bài gốc  
✅ **Đa ngôn ngữ:** Support cả tiếng Việt và tiếng Anh  
✅ **Responsive:** Hoạt động tốt trên mobile  

## Mở rộng trong tương lai

1. **Tích hợp LLM:** Sử dụng GPT/Gemini để sinh câu trả lời tự nhiên hơn
2. **Caching:** Cache kết quả để tăng tốc độ
3. **Analytics:** Theo dõi câu hỏi phổ biến
4. **Feedback:** Cho phép người dùng đánh giá câu trả lời
5. **Multi-language:** Tự động detect ngôn ngữ và trả lời phù hợp

## Liên hệ

Nếu có vấn đề, xem thêm tại:
- [BLOG_RAG_DEPLOYMENT.md](BLOG_RAG_DEPLOYMENT.md) - Hướng dẫn chi tiết
- [README_NEW.md](README_NEW.md) - Documentation đầy đủ

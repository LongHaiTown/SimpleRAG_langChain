"""
Script để embedding toàn bộ blog posts vào RAG system.
Chạy script này để tạo vector database từ các blog posts.
"""

import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.markdown_loader import load_and_split_markdown
from src.embedded_store import create_or_update_vector_db_from_collection, load_vector_db

# Đường dẫn đến thư mục blogs
BLOG_DIR = "c:/Code/DA_NetworkingPrograming/NetworkingPrograming/content/blogs"


def embed_all_blogs(blog_dir: str, persist_dir: str = "vectorstore"):
    """
    Embedding toàn bộ blog posts vào vector database.
    
    Args:
        blog_dir: Đường dẫn đến thư mục chứa các file markdown
        persist_dir: Thư mục lưu vector database
    """
    print("🚀 Starting blog embedding process...")
    print(f"📂 Blog directory: {blog_dir}")
    print(f"💾 Vector store directory: {persist_dir}")
    print("-" * 60)
    
    # 1. Load và split blogs thành chunks
    print("\n📖 Loading and splitting blog posts...")
    chunks = load_and_split_markdown(blog_dir, chunk_size=1000, chunk_overlap=200)
    
    if not chunks:
        print("❌ No blog posts found!")
        return
    
    # 2. Add doc_id cho toàn bộ blog collection
    collection_name = f"hugo_blogs_{os.path.basename(blog_dir)}"
    print(f"\n🔖 Collection name: {collection_name}")
    
    # 3. Create/Update vector database
    print(f"\n💿 Creating/updating vector database...")
    print(f"   Total chunks to embed: {len(chunks)}")
    
    # Sử dụng hàm mới cho collection
    vectordb = create_or_update_vector_db_from_collection(
        chunks, 
        collection_name=collection_name,
        persist_dir=persist_dir
    )
    
    print("\n" + "=" * 60)
    print("✅ Blog embedding completed successfully!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"   - Total blog posts processed: {len(set(c.metadata.get('filename') for c in chunks))}")
    print(f"   - Total chunks created: {len(chunks)}")
    print(f"   - Collection: {collection_name}")
    print(f"   - Vector store location: {persist_dir}")
    
    # 4. Test retrieval
    print("\n🧪 Testing retrieval...")
    test_query = "TCP socket"
    results = vectordb.similarity_search(test_query, k=3)
    print(f"   Query: '{test_query}'")
    print(f"   Found {len(results)} results:")
    for i, doc in enumerate(results, 1):
        title = doc.metadata.get('title', 'N/A')
        print(f"      {i}. {title}")
    
    return vectordb


if __name__ == "__main__":
    # Chạy embedding process
    vectordb = embed_all_blogs(BLOG_DIR)
    
    print("\n💡 Next steps:")
    print("   1. Start the API server: uvicorn api.app:app --reload --port 8000")
    print("   2. Test queries using /query_chunks or /query_both endpoints")
    print("   3. Update chat-widget.js with the correct API endpoint")

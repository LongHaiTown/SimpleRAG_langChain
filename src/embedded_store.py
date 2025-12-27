import hashlib
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def generate_doc_id(file_path):
    """Tạo doc_id duy nhất dựa trên nội dung file."""
    with open(file_path, "rb") as f:
        data = f.read()
    return hashlib.md5(data).hexdigest()

def create_or_update_vector_db(chunks, file_path, persist_dir="vectorstore"):
    """Upsert vectorstore cho 1 file PDF."""
    doc_id = generate_doc_id(file_path)

    # Gắn doc_id vào metadata của từng chunk
    for c in chunks:
        c.metadata["doc_id"] = doc_id
        c.metadata["source_file"] = file_path  # tiện để trace

    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)

    # Nếu doc_id đã tồn tại → xoá trước
    existing_ids = [f"{doc_id}_{i}" for i in range(10_000)]  # số đủ lớn
    vectordb.delete(ids=existing_ids)
    print(f"🗑️  Deleted old chunks for doc {file_path} (doc_id={doc_id})")

    # Add chunks mới
    vectordb.add_documents(chunks)
    print(f"✅ Upserted {len(chunks)} chunks for doc {file_path}")
    return vectordb


def create_or_update_vector_db_from_collection(chunks, collection_name, persist_dir="vectorstore"):
    """
    Upsert vectorstore cho một collection (ví dụ: blog posts).
    Dùng collection_name làm doc_id thay vì hash file content.
    
    Args:
        chunks: List of Document chunks
        collection_name: Tên collection (dùng làm doc_id)
        persist_dir: Thư mục lưu vector database
    """
    doc_id = hashlib.md5(collection_name.encode()).hexdigest()
    
    # Gắn doc_id vào metadata của từng chunk
    for c in chunks:
        c.metadata["doc_id"] = doc_id
        c.metadata["collection"] = collection_name
    
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    
    # Nếu doc_id đã tồn tại → xoá trước
    existing_ids = [f"{doc_id}_{i}" for i in range(10_000)]
    vectordb.delete(ids=existing_ids)
    print(f"🗑️  Deleted old chunks for collection {collection_name} (doc_id={doc_id})")
    
    # Add chunks mới
    vectordb.add_documents(chunks)
    print(f"✅ Upserted {len(chunks)} chunks for collection {collection_name}")
    return vectordb


def load_vector_db(persist_dir="vectorstore"):
    """Load lại vector DB đã lưu."""
    vectordb = Chroma(persist_directory=persist_dir, embedding_function=embeddings)
    return vectordb
import tempfile
import requests
from src.loader import load_and_split
from src.embedded_store import create_or_update_vector_db, load_vector_db
from src.retriever import build_topic_doc_graph

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# files = [
#     os.path.join(DATA_DIR, "Consensus Algorithms.pdf"),
#     os.path.join(DATA_DIR, "LangChain_usage.pdf"),
#     os.path.join(DATA_DIR, "RAG SoK.pdf"),
# ]

# # Update vectorstore cho từng file
# for file in files:
#     chunks = load_and_split(file)
#     vectordb = create_or_update_vector_db(chunks, file)



def download_temp_file(file_url: str) -> str:
    response = requests.get(file_url)
    response.raise_for_status()


    temp_path = os.path.join(tempfile.gettempdir(), "test")

    with open(temp_path, "wb") as f:
        f.write(response.content)

    print(f"✅ File downloaded: {temp_path}")
    return temp_path

def ingest_from_supabase_urls(file_urls: list):
    for url in file_urls:
        local_path = download_temp_file(url)
        chunks = load_and_split(local_path)
        vectordb = create_or_update_vector_db(chunks, local_path)
        print(f"✅ VectorDB updated for: {url}")
    

ingest_from_supabase_urls(["https://cysokmjkkmitxzagoqjh.supabase.co/storage/v1/object/sign/documents/69e130e0-c26c-471e-8512-db516de6c35b/uncategorized/1759899572510_Image_Classification_Based_On_CNN_A_Survey.pdf?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV84MGM2OTQ5Zi0zNTQxLTRlZGItYjllOS1lZDc3YjY1YjNmZTEiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJkb2N1bWVudHMvNjllMTMwZTAtYzI2Yy00NzFlLTg1MTItZGI1MTZkZTZjMzViL3VuY2F0ZWdvcml6ZWQvMTc1OTg5OTU3MjUxMF9JbWFnZV9DbGFzc2lmaWNhdGlvbl9CYXNlZF9Pbl9DTk5fQV9TdXJ2ZXkucGRmIiwiaWF0IjoxNzU5OTAwMTk2LCJleHAiOjE3NTk5MDM3OTZ9.9aqlCVsobph40xtoClFQ1Sr2IFSB_vKedeLKwl1iiAQ"])



# # Test load lại
# vectordb = load_vector_db()
# print("Vector DB ready:", vectordb)

# graph = build_topic_doc_graph(vectordb, ["RAG"], top_k=3, output_file="topic_doc_graph.json")

# uvicorn api.app:app --reload --port 8000
# streamlit run ui/streamlit_app.py


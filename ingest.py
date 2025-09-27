from src.loader import load_and_split
from src.embedded_store import create_or_update_vector_db, load_vector_db
from src.retriever import build_topic_doc_graph

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

files = [
    os.path.join(DATA_DIR, "Consensus Algorithms.pdf"),
    os.path.join(DATA_DIR, "LangChain_usage.pdf"),
    os.path.join(DATA_DIR, "RAG SoK.pdf"),
]


# # Update vectorstore cho từng file
# for file in files:
#     chunks = load_and_split(file)
#     vectordb = create_or_update_vector_db(chunks, file)

# # Test load lại
vectordb = load_vector_db()
print("Vector DB ready:", vectordb)

graph = build_topic_doc_graph(vectordb, ["RAG"], top_k=3, output_file="topic_doc_graph.json")

# uvicorn api.app:app --reload --port 8000
# streamlit run ui/streamlit_app.py

from collections import defaultdict
import json

def retrieve_chunks(vectordb, query: str, k: int = 3):
    """Truy vấn theo chunk (fine-grained)."""
    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    docs = retriever.get_relevant_documents(query)
    return docs

def retrieve_documents(vectordb, query: str, k: int = 2, chunk_k: int = 5):
    """Truy vấn theo document (gom chunk -> vote)."""
    retriever = vectordb.as_retriever(search_kwargs={"k": chunk_k})
    docs = retriever.get_relevant_documents(query)

    doc_scores = defaultdict(int)
    for d in docs:
        src = d.metadata.get("source", "unknown")
        doc_scores[src] += 1
    
    ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:k]
    return ranked_docs

def query_both_levels(vectordb, query: str, k_doc: int = 2, k_chunk: int = 3):
    """Kết hợp document-level và chunk-level retrieval."""
    chunk_docs = retrieve_chunks(vectordb, query, k_chunk)
    ranked_docs = retrieve_documents(vectordb, query, k_doc, chunk_k=k_chunk*2)
    return {"documents": ranked_docs, "chunks": chunk_docs}


def show_results(docs):
    """Hiển thị kết quả chunk ra console."""
    for i, doc in enumerate(docs, start=1):
        print(f"\n--- Chunk {i} ---")
        print(doc.page_content[:500])  # chỉ in 500 ký tự đầu
        print(f"(source: {doc.metadata})")
        

# def build_topic_doc_graph(vectordb, topics, top_k=5, output_file="topic_doc_graph.json"):
#     nodes = []
#     edges = []
#     node_ids = set()

#     for topic in topics:
#         # Add topic node nếu chưa có
#         if topic not in node_ids:
#             nodes.append({"id": topic, "type": "topic", "label": topic})
#             node_ids.add(topic)

#         # Query top-k docs liên quan
#         docs = vectordb.similarity_search(topic, k=top_k)
#         for doc in docs:
#             doc_id = doc.metadata.get("doc_id", None)
#             source = doc.metadata.get("source_file", "unknown")

#             if not doc_id:
#                 continue 

#             if doc_id not in node_ids:
#                 nodes.append({"id": doc_id, "type": "document", "label": source})
#                 node_ids.add(doc_id)

#             edges.append({"source": topic, "target": doc_id})

#     graph = {"nodes": nodes, "edges": edges}

#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(graph, f, indent=2, ensure_ascii=False)

#     print(f"✅ Exported graph JSON to {output_file}")
#     return graph

def build_topic_doc_graph(vectordb, topics: list[str], top_k: int = 5):
    """
    Xây dựng graph JSON topic ↔ document từ vectorstore.
    """
    nodes = []
    edges = []
    node_ids = set()

    for topic in topics:
        # Add topic node nếu chưa có
        if topic not in node_ids:
            nodes.append({"id": topic, "type": "topic", "label": topic})
            node_ids.add(topic)

        # Query top-k docs liên quan
        docs = vectordb.similarity_search(topic, k=top_k)
        for doc in docs:
            doc_id = doc.metadata.get("doc_id", None)
            source = doc.metadata.get("source_file", "unknown")

            if not doc_id:
                continue

            # Add document node nếu chưa có
            if doc_id not in node_ids:
                nodes.append({"id": doc_id, "type": "document", "label": source})
                node_ids.add(doc_id)

            # Add edge topic ↔ doc
            edges.append({"source": topic, "target": doc_id})

    return {"nodes": nodes, "edges": edges}
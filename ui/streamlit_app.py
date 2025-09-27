import streamlit as st
import requests
from pyvis.network import Network
import json

BASE_URL = "http://127.0.0.1:8000"

# Sidebar navigation
st.sidebar.title("🔗 Navigation")
page = st.sidebar.radio("Go to:", ["Retriever", "Show Documents", "Knowledge Graph"])

# -------------------------------
# 🔎 Retriever Page
# -------------------------------
if page == "Retriever":
    st.title("📚 Research Paper Retriever")

    query = st.text_input("Enter your question:")

    mode = st.selectbox(
        "Choose retrieval mode:",
        ["Chunks only", "Documents only", "Both"]
    )

    top_k_chunk = st.slider("Number of chunks", 1, 10, 3)
    top_k_doc = st.slider("Number of documents", 1, 5, 2)

    if st.button("Search") and query:
        if mode == "Chunks only":
            url = f"{BASE_URL}/query_chunks"
            params = {"q": query, "k": top_k_chunk}
        elif mode == "Documents only":
            url = f"{BASE_URL}/query_documents"
            params = {"q": query, "k": top_k_doc, "chunk_k": top_k_chunk}
        else:
            url = f"{BASE_URL}/query_both"
            params = {"q": query, "k_doc": top_k_doc, "k_chunk": top_k_chunk}

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            if mode == "Chunks only":
                st.subheader("Relevant Chunks")
                for res in data["chunks"]:
                    st.markdown(f"**Chunk {res['chunk_id']}**")
                    st.write(res["content"])
                    st.caption(res["metadata"])

            elif mode == "Documents only":
                st.subheader("Relevant Documents")
                for res in data["documents"]:
                    st.markdown(f"- **{res['doc_source']}** (score={res['score']})")

            else:
                st.subheader("Relevant Documents")
                for doc, score in data["documents"]:
                    st.markdown(f"- **{doc}** (score={score})")

                st.subheader("Relevant Chunks")
                for res in data["chunks"]:
                    st.markdown(f"**Chunk {res['chunk_id']}**")
                    st.write(res["content"][:400] + "...")
                    st.caption(res["metadata"])
        else:
            st.error("API request failed!")

# -------------------------------
# 📂 Show Documents Page
# -------------------------------
elif page == "Show Documents":
    st.title("📂 All Research Papers in VectorStore")

    if st.button("Refresh"):
        response = requests.get(f"{BASE_URL}/list_documents")
        if response.status_code == 200:
            data = response.json()
            docs = data["documents"]

            if not docs:
                st.warning("⚠️ No documents found in vectorstore.")
            else:
                st.subheader(f"Found {len(docs)} documents:")
                for doc in docs:
                    st.markdown(f"- **doc_id**: `{doc['doc_id']}`  \n📄 {doc['source_file']}")
        else:
            st.error("❌ Failed to fetch documents from API.")

# -------------------------------
# 🕸 Knowledge Graph Page
# -------------------------------
elif page == "Knowledge Graph":
    st.title("🕸 Topic ↔ Document Knowledge Graph")

    topics_input = st.text_area(
        "Enter topics (one per line):",
        value="RAG\nCryptanalysis\nConsensus Algorithm"
    )

    top_k = st.slider("Number of documents per topic", 1, 10, 5)

    if st.button("Generate Graph"):
        topics = [t.strip() for t in topics_input.split("\n") if t.strip()]
        if not topics:
            st.warning("⚠️ Please enter at least one topic")
        else:
            response = requests.post(
                f"{BASE_URL}/graph?top_k={top_k}",
                json=topics
            )
            if response.status_code == 200:
                graph_data = response.json()

                # Build Pyvis graph
                net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")

                # Add nodes
                for node in graph_data["nodes"]:
                    if node["type"] == "topic":
                        net.add_node(node["id"], label=node["label"],
                                     color="orange", shape="ellipse")
                    else:
                        net.add_node(node["id"], label=node["label"],
                                     color="lightblue", shape="box")

                # Add edges
                for edge in graph_data["edges"]:
                    net.add_edge(edge["source"], edge["target"])

                net.save_graph("graph.html")
                st.components.v1.html(open("graph.html", "r", encoding="utf-8").read(), height=650)
            else:
                st.error("❌ Failed to fetch graph from API.")

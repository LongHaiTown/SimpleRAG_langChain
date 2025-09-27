import streamlit as st
from pyvis.network import Network
import json

st.title("🕸 Knowledge Graph: Topics ↔ Documents")

# Load graph JSON
with open("topic_doc_graph.json", "r", encoding="utf-8") as f:
    graph_data = json.load(f)

# Tạo Pyvis graph
net = Network(height="600px", width="100%", notebook=False, bgcolor="#222222", font_color="white")

# Add nodes
for node in graph_data["nodes"]:
    if node["type"] == "topic":
        net.add_node(node["id"], label=node["label"], color="orange", shape="ellipse")
    else:
        net.add_node(node["id"], label=node["label"], color="lightblue", shape="box")

# Add edges
for edge in graph_data["edges"]:
    net.add_edge(edge["source"], edge["target"])

# Xuất ra HTML
net.save_graph("graph.html")

# Hiển thị trong Streamlit (iframe)
st.components.v1.html(open("graph.html", "r", encoding="utf-8").read(), height=650)

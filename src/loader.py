from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

semantic_splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="gradient",
    breakpoint_threshold_amount=0.8,
)

def load_and_split(file_path: str):
    """Load 1 file PDF và split thành chunks bằng Semantic Splitter."""
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    chunks = semantic_splitter.split_documents(docs)
    return chunks

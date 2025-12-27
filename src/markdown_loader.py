"""
Markdown Loader cho Hugo Blog Posts
Hỗ trợ đọc và xử lý các file markdown từ Hugo blog.
"""

import os
import re
from typing import List
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

class HugoBlogLoader:
    """Loader cho Hugo blog posts (markdown files)."""
    
    def __init__(self, blog_dir: str):
        """
        Args:
            blog_dir: Đường dẫn đến thư mục chứa các file markdown
        """
        self.blog_dir = blog_dir
        
    def load(self) -> List[Document]:
        """Load tất cả các file markdown trong blog_dir."""
        documents = []
        
        for filename in os.listdir(self.blog_dir):
            if filename.endswith('.md') and filename != '_index.md':
                filepath = os.path.join(self.blog_dir, filename)
                doc = self._load_single_file(filepath)
                if doc:
                    documents.append(doc)
        
        print(f"✅ Loaded {len(documents)} blog posts from {self.blog_dir}")
        return documents
    
    def _load_single_file(self, filepath: str) -> Document:
        """Load một file markdown và trích xuất metadata."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter (YAML between --- markers)
            frontmatter, body = self._parse_frontmatter(content)
            
            # Extract metadata
            title = frontmatter.get('title', os.path.basename(filepath))
            date = frontmatter.get('date', '')
            tags = frontmatter.get('tags', [])
            
            # Create metadata
            metadata = {
                'source': filepath,
                'filename': os.path.basename(filepath),
                'title': title,
                'date': date,
                'tags': ', '.join(tags) if isinstance(tags, list) else str(tags),  # Convert list to string
                'type': 'blog_post'
            }
            
            return Document(page_content=body, metadata=metadata)
            
        except Exception as e:
            print(f"⚠️  Error loading {filepath}: {e}")
            return None
    
    def _parse_frontmatter(self, content: str):
        """Parse YAML frontmatter từ markdown file."""
        frontmatter = {}
        body = content
        
        # Check if file has frontmatter (--- ... ---)
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1]
                body = parts[2].strip()
                
                # Parse simple YAML (title, date, tags)
                for line in frontmatter_text.split('\n'):
                    line = line.strip()
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Handle tags as list
                        if key == 'tags' and value.startswith('['):
                            value = [t.strip().strip('"').strip("'") 
                                   for t in value.strip('[]').split(',')]
                        
                        frontmatter[key] = value
        
        return frontmatter, body


def load_and_split_markdown(blog_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Load tất cả blog posts và split thành chunks.
    
    Args:
        blog_dir: Đường dẫn đến thư mục blogs
        chunk_size: Kích thước mỗi chunk (số ký tự)
        chunk_overlap: Số ký tự overlap giữa các chunks
        
    Returns:
        List[Document]: Danh sách các chunks
    """
    # Load documents
    loader = HugoBlogLoader(blog_dir)
    documents = loader.load()
    
    # Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    
    print(f"✅ Split into {len(chunks)} chunks")
    return chunks


if __name__ == "__main__":
    # Test the loader
    blog_dir = "c:/Code/DA_NetworkingPrograming/NetworkingPrograming/content/blogs"
    chunks = load_and_split_markdown(blog_dir)
    
    print(f"\n--- Sample chunk ---")
    if chunks:
        print(f"Title: {chunks[0].metadata.get('title')}")
        print(f"Content: {chunks[0].page_content[:200]}...")

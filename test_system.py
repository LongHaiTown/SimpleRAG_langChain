"""
Script test để kiểm tra hệ thống RAG Blog Chat
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test health check endpoint"""
    print("🧪 Testing /health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        print("   ⚠️  Make sure API server is running:")
        print("   uvicorn api.app:app --reload --port 8000")
        return False

def test_chat(question, k=3):
    """Test chat endpoint"""
    print(f"\n🧪 Testing /chat endpoint...")
    print(f"   Question: {question}")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json={"question": question, "k": k},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Chat request successful")
            print(f"\n📝 Answer:")
            print(f"   {data['answer'][:200]}..." if len(data['answer']) > 200 else data['answer'])
            
            if data.get('sources'):
                print(f"\n📚 Sources ({data['total_sources']}):")
                for i, source in enumerate(data['sources'], 1):
                    print(f"   {i}. {source['title']}")
                    print(f"      URL: {source['url']}")
                    print(f"      Excerpt: {source['excerpt'][:100]}...")
            
            return True
        else:
            print(f"❌ Chat request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat request error: {e}")
        return False

def test_query_chunks():
    """Test query_chunks endpoint"""
    print(f"\n🧪 Testing /query_chunks endpoint...")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/query_chunks",
            params={"q": "TCP socket", "k": 2}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Query chunks successful")
            print(f"   Found {len(data['chunks'])} chunks")
            
            for chunk in data['chunks'][:2]:  # Show first 2
                print(f"\n   Chunk {chunk['chunk_id']}:")
                print(f"      {chunk['content'][:150]}...")
                if chunk['metadata'].get('title'):
                    print(f"      Title: {chunk['metadata']['title']}")
            
            return True
        else:
            print(f"❌ Query chunks failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Query chunks error: {e}")
        return False

def test_list_documents():
    """Test list_documents endpoint"""
    print(f"\n🧪 Testing /list_documents endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/list_documents")
        
        if response.status_code == 200:
            data = response.json()
            docs = data.get('documents', [])
            print(f"✅ List documents successful")
            print(f"   Total documents: {len(docs)}")
            
            if docs:
                print(f"\n   Sample documents:")
                for doc in docs[:3]:  # Show first 3
                    print(f"      - {doc['source_file']}")
                    print(f"        Doc ID: {doc['doc_id'][:16]}...")
            
            return True
        else:
            print(f"❌ List documents failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ List documents error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("🚀 RAG Blog Chat - Integration Tests")
    print("=" * 60)
    
    # Test 1: Health Check
    if not test_health():
        print("\n⚠️  API server is not running. Please start it first:")
        print("   cd C:\\Code\\DACN_MindMapNote\\SimpleRAG_langChain")
        print("   uvicorn api.app:app --reload --port 8000")
        return
    
    # Test 2: List Documents (check if vectorstore has data)
    if not test_list_documents():
        print("\n⚠️  No documents found in vectorstore. Please run embedding:")
        print("   python embed_blog_posts.py")
        return
    
    # Test 3: Query Chunks
    test_query_chunks()
    
    # Test 4: Chat Endpoint
    test_questions = [
        "TCP 3-way handshake là gì?",
        "Sự khác biệt giữa TCP và UDP",
        "Code mẫu Java Socket Server"
    ]
    
    for question in test_questions:
        test_chat(question, k=3)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    
    print("\n💡 Next steps:")
    print("   1. Open http://localhost:1313/NetworkingPrograming/blogs/")
    print("   2. Click the chat widget icon")
    print("   3. Try asking questions about blog content")
    print("   4. Verify sources are linked correctly")

if __name__ == "__main__":
    main()

import os
from supabase import create_client, Client
from src.loader import load_and_split
from src.embedded_store import create_or_update_vector_db, load_vector_db
from src.retriever import build_topic_doc_graph
import tempfile
import requests

url = "https://cysokmjkkmitxzagoqjh.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN5c29rbWpra21pdHh6YWdvcWpoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODk5MDAxMiwiZXhwIjoyMDc0NTY2MDEyfQ.iPiCrRBQL9zYl4MBZjljB7TMdfHDeccbKb1q1yE97Bw"
supabase: Client = create_client(url, key)

'''
Testing Connection

print("✅ Supabase client initialized:", supabase is not None)

response = supabase.table("documents").select("*").limit(1).execute()
print(response)

res = supabase.storage.from_("documents").list(
    "69e130e0-c26c-471e-8512-db516de6c35b/uncategorized"
)
print("📦 Files:", res)

'''

def download_temp_file_from_res(bucket: str, folder_prefix: str, file_obj: dict) -> str:
    file_name = file_obj["name"]
    full_path = f"{folder_prefix}/{file_name}".strip("/")  

    signed = supabase.storage.from_(bucket).create_signed_url(full_path, 3600)
    if not signed or "signedURL" not in signed:
        raise Exception(f"❌ Không thể tạo signed URL cho file: {file_name}")

    file_url = signed["signedURL"]

    response = requests.get(file_url)
    response.raise_for_status()

    temp_path = os.path.join(tempfile.gettempdir(), file_name)
    with open(temp_path, "wb") as f:
        f.write(response.content)

    print(f"✅ File downloaded: {temp_path} ({file_obj['metadata']['size']} bytes)")
    return temp_path

def download_all_files(bucket: str, folder_prefix: str = ""):
    """
    Duyệt và tải tất cả file trong thư mục Supabase Storage.
    """
    files = supabase.storage.from_(bucket).list(folder_prefix)
    local_files = []
    print(files)

    for file_obj in files:
        if file_obj.get("metadata") is None:
            # Nếu là folder con → có thể đệ quy tại đây nếu muốn
            continue
        try:
            local_path = download_temp_file_from_res(bucket,folder_prefix, file_obj)
            local_files.append(local_path)
        except Exception as e:
            print(f"⚠️ Lỗi tải {file_obj['name']}: {e}")

    return local_files

if __name__ == "__main__":
    # ví dụ: bucket = "documents", folder_prefix = "69e130e0-c26c-471e-8512-db516de6c35b/uncategorized"
    bucket = "documents"
    folder_prefix = "69e130e0-c26c-471e-8512-db516de6c35b/uncategorized"
    files = download_all_files(bucket, folder_prefix)
    print("\n📦 Files downloaded locally:")
    for f in files:
        print(" -", f)

    for file in files:
        chunks = load_and_split(file)
        vectordb = create_or_update_vector_db(chunks, file)

    
# Update vectorstore cho từng file


# def ingest_from_supabase_urls(file_urls: list):
#     for url in file_urls:
#         local_path = download_temp_file(url)
#         chunks = load_and_split(local_path)
#         vectordb = create_or_update_vector_db(chunks, local_path)
#         print(f"✅ VectorDB updated for: {url}")


# # Lấy danh sách file
# res = supabase.storage.from_("documents").list()
# for file in res:
#     signed = supabase.storage.from_("documents/69e130e0-c26c-471e-8512-db516de6c35b/uncategorized").create_signed_url(file["name"], 3600)
#     ingest_from_supabase_urls([signed["signedURL"]])

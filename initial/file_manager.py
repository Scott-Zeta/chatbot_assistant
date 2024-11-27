import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

vs_id = os.getenv("VECTOR_STORAGE_ID")

def upload_file_to_vector_store(vs_id, file_streams):
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vs_id, files=file_streams
)
    while True:
        if file_batch.status == "completed":
            print("File Uploaded completed")
            break
        elif file_batch.status == "in_progress":
            print("File Uploading...")
            time.sleep(5)
        else:
            print(file_batch.status)
            break
    print(file_batch.file_counts)
    
if vs_id:
    # Retrieve Vector Storage
    vector_store = client.beta.vector_stores.retrieve(vector_store_id=vs_id)
    vector_store_files = client.beta.vector_stores.files.list(vector_store_id =vs_id)
    print("====Vector Store Retrieved====")
    print(f"ID: {vector_store.id}")
    print(f"Total file number: {vector_store.file_counts.total}")
    print("====Vector Store Files====")
    for file in vector_store_files.data:
        print(file.id)
else:
    # Create Vector Storage
    new_vector_store_name = os.getenv("VECTOR_STORAGE_NAME") or "New Vector Store"
    vector_store = client.beta.vector_stores.create(name=new_vector_store_name)
    vs_id = vector_store.id
    print("====New Vector Store Created====")
    print(f"ID: {vector_store.id}")
    print(f"Name: {vector_store.name}")

# Add File to Vector Storage

if vector_store.id:
    file_paths = ["data/FS Community connections DOCX.docx", "data/FS Early Connections PDF.pdf"]
    file_streams = [open(path, "rb") for path in file_paths]
    upload_file_to_vector_store(vector_store.id, file_streams)
else:
    print("Vector Store Not Found")
  

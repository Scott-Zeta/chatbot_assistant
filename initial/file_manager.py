import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

vs_id = os.getenv("VECTOR_STORAGE_ID")

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
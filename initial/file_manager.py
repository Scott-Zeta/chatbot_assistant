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
    print(vector_store)
    print("====Vector Store Files====")
    print(vector_store_files)
else:
    # Create Vector Storage
    pass
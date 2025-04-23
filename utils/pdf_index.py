import os
from llama_index.core.readers import SimpleDirectoryReader
from llama_index.core.indices.vector_store import GPTVectorStoreIndex
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core import load_index_from_storage

PERSIST_DIR = "index_store"

def create_or_load_index(upload_folder="pdfs", force_recreate=False):
    if force_recreate or not os.path.exists(PERSIST_DIR) or not os.listdir(PERSIST_DIR):
        print("Creating new index...")
        documents = SimpleDirectoryReader(upload_folder).load_data()
        index = GPTVectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        print("Loading index from storage...")
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
    return index

def save_uploaded_pdfs(uploaded_files, upload_folder):
    new_files_uploaded = False
    for uploaded_file in uploaded_files:
        file_path = os.path.join(upload_folder, uploaded_file.name)
        if not os.path.exists(file_path):
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            new_files_uploaded = True
    return new_files_uploaded

def has_new_files(upload_folder, uploaded_files):
    return any(not os.path.exists(os.path.join(upload_folder, f.name)) for f in uploaded_files)

import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.embeddings.embedding_manager import EmbeddingManager, POL_DOCS, PROD_DOCS
from app.retrievers.vector_store import VectorStore
from langchain_core.documents import Document
from typing import List

def build_collection(collection_name, docs: List[Document], embedding_manager: EmbeddingManager):
    vector_store = VectorStore(collection_name=collection_name)

    if vector_store.collection.count() > 0:
        print(f"[SKIP LOADING] Collection '{collection_name}' already exists.")
        return 
    
    texts = [doc.page_content for doc in docs]
    embeddings = embedding_manager.generate_embeddings(texts)
    vector_store.add_documents(docs, embeddings)
    print(f"[DONE] Built collection '{collection_name}'")


def load_all_collections():
    embedding_manager = EmbeddingManager()

    build_collection("policy", POL_DOCS, embedding_manager)
    build_collection("product", PROD_DOCS, embedding_manager)
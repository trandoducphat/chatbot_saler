import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.embeddings.embedding_manager import EmbeddingManager
from app.retrievers.vector_store import VectorStore
from app.retrievers.retriever import RAGRetriever
from app.retrievers.registry import init_retrievers
from app.graph.graph_builder import build_graph



def init_state() -> ChatState:
    return {"user_message": "" }

def boostrap_chat_app():
    embedding_manager = EmbeddingManager()
    policy_store = VectorStore("policy")
    product_store = VectorStore("product")

    if policy_store.collection.count() == 0 or product_store.collection.count() == 0:
        raise RuntimeError("Vector store is empty. Run load_all_collections() to load")
    
    policy_retriever = RAGRetriever(policy_store, embedding_manager)
    product_retriever = RAGRetriever(product_store, embedding_manager)

    init_retrievers(policy_retriever=policy_retriever, product_retriever=product_retriever)
    graph = build_graph()
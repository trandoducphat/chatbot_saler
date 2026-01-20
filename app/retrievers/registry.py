import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from typing import Optional
from app.retrievers.retriever import RAGRetriever

_policy_retriever: Optional[RAGRetriever] = None
_product_retriever: Optional[RAGRetriever] = None

def init_retrievers(policy_retriever: RAGRetriever, product_retriever: RAGRetriever):
    global _policy_retriever, _product_retriever
    _product_retriever = product_retriever
    _policy_retriever = policy_retriever


def get_policy_retriever() -> RAGRetriever:
    if _policy_retriever is None:
        raise RuntimeError("Policy retriever not initialized")
    return _policy_retriever

def get_product_retriever() -> RAGRetriever:
    if _product_retriever is None:
        raise RuntimeError("Product retriever not initialized")
    return _product_retriever

def is_product_retriver_initialized():
    return _product_retriever is not None

def is_policy_retriever_initialized():
    return _policy_retriever is not None
import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)


from langgraph.graph import StateGraph, END
from app.graph.state import ChatState
from app.graph.routers import route_by_intent
from app.intent.intent_router import dectect_intent
from app.graph.nodes.fast_answer import fast_answer_node
from app.graph.nodes.ask_clarify import ask_clarify_node
from app.graph.nodes.finalize import finalize_node
from app.graph.nodes.rag_reason import rag_reason_node
from app.graph.nodes.recommend_car import recommend_car_node
from app.graph.nodes.retrieve_policy import retrieve_policy_node
from app.graph.nodes.retrieve_product import retrieve_product_node
from app.graph.nodes.retrieve_info import retrieve_info_node

def build_graph():
    graph = StateGraph(ChatState)

    graph.add_node("detect_intent", dectect_intent)

    graph.add_node("fast_answer", fast_answer_node)
    graph.add_node("ask_clarify", ask_clarify_node)
    graph.add_node("finalize", finalize_node)
    graph.add_node("rag_reason", rag_reason_node)
    graph.add_node("recommend_car", recommend_car_node)
    graph.add_node("retrieve_policy", retrieve_policy_node)
    graph.add_node("retrieve_product", retrieve_product_node)
    graph.add_node("retrieve_info", retrieve_info_node)

    graph.set_entry_point("detect_intent")

    graph.add_conditional_edges(
        "detect_intent",
        route_by_intent,
        {
            "fast_answer": "fast_answer",
            "ask_clarify": "ask_clarify",
            "rag_reason": "rag_reason",
            "recommend_car": "recommend_car",
            "retrieve_policy": "retrieve_policy",
            "retrieve_product": "retrieve_product",
            "retrieve_info": "retrieve_info"
        }
    )
  
    graph.add_edge("fast_answer", END)
    graph.add_edge("ask_clarify", END)
    graph.add_edge("rag_reason", END)
    graph.add_edge("recommend_car", END)
    graph.add_edge("retrieve_policy", END)
    graph.add_edge("retrieve_product", END)
    graph.add_edge("retrieve_info", END)

    return graph.compile()
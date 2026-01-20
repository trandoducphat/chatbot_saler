import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.intent.base import Intent

def route_by_intent(state: ChatState) -> str:
    if state.intent == Intent.GREETING or state.intent == Intent.GOODBYE:
        return "fast_answer"
    
    if state.intent == Intent.CONFIRM_SELECTION:
        if state.selected_car:
            return "finalize"
        return "ask_clarify"
    
    if state.intent == Intent.ASK_POLICY:
        return "retrieve_policy"
    
    if state.intent == Intent.COMPARE_CARS:
        return "retrieve_product"

    if state.intent == Intent.ASK_CAR_INFO:
        return "retrieve_info"
    
    if state.intent == Intent.ASK_RECOMMENDATION or state.intent == Intent.FILTER_BY_BRAND or state.intent == Intent.FILTER_BY_PRICE:
        return "recommend_car"
    
    return "rag_reason"
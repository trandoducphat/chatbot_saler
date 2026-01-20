import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.intent.base import Intent
from app.intent.llm_intent import llm_detect_intent
from app.intent.rule_intent import detect_rule_intent
from app.graph.state import ChatState

def dectect_intent(state: ChatState) -> ChatState:
    rule_intent = detect_rule_intent(state.user_message)
    if rule_intent:
        state.intent = rule_intent
        return state

    llm_intent = llm_detect_intent(state.user_message, str(state.intent), str(state.selected_car))
    state.intent = llm_intent
    return state
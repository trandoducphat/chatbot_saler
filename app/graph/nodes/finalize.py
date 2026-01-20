import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.intent.base import Intent

def finalize_node(state: ChatState) -> ChatState:
    state.history.append("User: " + state.user_message)

    car = state.selected_car
    state.response = f"Bạn đã chốt mẫu xe {car['brand']} {car['model']}. Nhân viên sẽ sớm liên hệ với bạn!"

    state.history.append("Bot: " + state.response)

    return state
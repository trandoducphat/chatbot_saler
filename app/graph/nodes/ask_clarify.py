import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.intent.base import Intent

def ask_clarify_node(state: ChatState) -> ChatState:
    state.history.append("User: " + state.user_message)

    state.response = "Tôi vẫn chưa xác định được mẫu xe mà bạn đang đề cập đến. Hãy nêu ra những tiêu chí chọn xe của bạn để tôi có thể hỗ trợ nhé!"
    
    state.history.append("Bot: " + state.response)

    return state
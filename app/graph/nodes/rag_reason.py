import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.intent.base import Intent

def rag_reason_node(state: ChatState) -> ChatState:
    state.history.append("User: " + state.user_message)

    state.response = "Tôi chưa hiểu ý định của bạn. Nếu cần hỗ trợ thêm về thông tin xe hoặc chính sách công ty, vui lòng nêu rõ thắc mắc của bạn để tôi có thể hỗ trợ nhé."

    state.history.append("Bot: " + state.response)
    return state
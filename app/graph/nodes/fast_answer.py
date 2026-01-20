import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.intent.base import Intent

def fast_answer_node(state: ChatState) -> ChatState:
    state.history.append("User: " + state.user_message)

    if state.intent == Intent.GREETING:
        state.response = "Chào bạn, tôi là trợ lý ảo chăm sóc khách hàng. Tôi sẵn sàng hỗ trợ bạn tư vấn, chọn xe và báo giá chi tiết. Bạn đang cần hỗ trợ gì ạ?"
    
    elif state.intent == Intent.GOODBYE:
        state.response = "Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi. Nếu cần hỗ trợ thêm, đừng ngần ngại quay lại nhé. Hẹn gặp lại!"
    
    state.history.append("Bot: " + state.response)

    return state
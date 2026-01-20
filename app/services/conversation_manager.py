import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState

class ConversationManager:
    def __init__(self):
        self.session = {}

    def new_conversation(self, conversation_id: str) -> ChatState:
        state = ChatState()
        self.session[conversation_id] = state
        return state
    
    def get_state(self, conversation_id: str) -> ChatState:
        return self.session.get(conversation_id)
    
    def reset(self, conversation_id: str):
        self.session[conversation_id] = ChatState()
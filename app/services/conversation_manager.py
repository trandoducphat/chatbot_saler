import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState

class ConversationManager:
    def __init__(self, state_factory):
        self.sessions: dict[str, ChatState] = {}
        self.state_factory = state_factory

    def new_conversation(self, conversation_id: str) -> ChatState:
        state = self.state_factory()
        self.sessions[conversation_id] = state
        return state

    def reset(self, conversation_id: str):
        self.sessions[conversation_id] = self.state_factory()
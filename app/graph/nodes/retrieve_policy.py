import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.graph.chains.retrieve_policy_chain import retrieve_policy_chain

def retrieve_policy_node(state: ChatState) -> ChatState:
    state.history.append("User: " + state.user_message)
    
    new_state = retrieve_policy_chain.invoke(state)

    new_state.history.append("Bot: " + new_state.response)
    return new_state
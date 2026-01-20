import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.intent.base import Intent
from app.graph.chains.recommend_car_chain import recommend_car_chain

def recommend_car_node(state: ChatState) -> ChatState:
    state.history.append("User: " + state.user_message)

    new_state = recommend_car_chain.invoke(state)

    state.history.append("Bot: " + state.response)

    return new_state
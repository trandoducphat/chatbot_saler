import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.intent.base import Intent
from app.graph.chains.retrieve_products_chain import retrieve_products_chain

def retrieve_product_node(state: ChatState) -> ChatState:
    state.history.append("User: " + state.user_message)

    new_state = retrieve_products_chain.invoke(state)

    new_state.history.append("Bot: " + new_state.response)

    return new_state
import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.intent.base import Intent
from dataclasses import dataclass, field

@dataclass
class ChatState:
    user_message: str

    intent: Intent | None = None

    history: list[str] = field(default_factory=list)

    selected_car: dict = field(default_factory=dict)
    compared_car: list[dict] = field(default_factory=list)

    retrieved_docs: list[dict] = field(default_factory=list)
    policy_context: str = ""

    response: str = ""
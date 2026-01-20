from .fast_answer import fast_answer_node
from .finalize import finalize_node
from .ask_clarify import ask_clarify_node
from .retrieve_policy import retrieve_policy_node
from .retrieve_product import retrieve_product_node
from .recommend_car import recommend_car_node
# from .rag_reason import rag_reason_node

NODE_REGISTRY = {
    "fast_answer": fast_answer,
    "finalize": finalize,
    "ask_clarify": ask_clarify,
    "retrieve_policy": retrieve_policy,
    "retrieve_product": retrieve_product,
    "recommend_car": recommend_car,
    # "rag_reason": rag_reason,
}

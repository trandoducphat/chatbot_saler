import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.retrievers.registry import get_product_retriever
from langchain_core.runnables import RunnableLambda

def retrieve_products_docs(state: ChatState) -> ChatState:
    product_retriver = get_product_retriever()
    retrieved_products = product_retriver.retrieve(state.user_message, 2, 0.0)

    state.compared_car = retrieved_products
    return state

def normalize_product(p):
    if hasattr(p, "metadata") and isinstance(p.metadata, dict):
        return p.metadata

    if isinstance(p, dict) and "metadata" in p and isinstance(p["metadata"], dict):
        return p["metadata"]

    if isinstance(p, dict):
        return p

    raise TypeError(f"Unsupported product type: {type(p)}")


def build_compare_table(state: ChatState) -> ChatState:
    if not state.compared_car or len(state.compared_car) != 2:
        raise ValueError(
            "Tôi chưa xác định được 2 sản phẩm mà bạn đang so sánh. "
            "Hãy mô tả rõ nhất về thông tin (tên hãng + tên mẫu) của 2 sản phẩm."
        )

    p1 = normalize_product(state.compared_car[0])
    p2 = normalize_product(state.compared_car[1])

    fields = sorted(set(p1.keys()) | set(p2.keys()))

    def get_title(p: dict) -> str:
        brand = str(p.get("brand", ""))
        model = str(p.get("model", ""))
        title = f"{brand} {model}".strip()
        return title if title else "Sản phẩm"

    title1 = get_title(p1)
    title2 = get_title(p2)

    col1_width = max(len("Thông số"), *(len(f) for f in fields))
    col2_width = max(len(title1), *(len(str(p1.get(f, ""))) for f in fields))
    col3_width = max(len(title2), *(len(str(p2.get(f, ""))) for f in fields))

    def line():
        return (
            "+" + "-" * (col1_width + 2) +
            "+" + "-" * (col2_width + 2) +
            "+" + "-" * (col3_width + 2) + "+"
        )

    rows = []
    rows.append(line())
    rows.append(
        f"| {'Thông số'.ljust(col1_width)} "
        f"| {title1.ljust(col2_width)} "
        f"| {title2.ljust(col3_width)} |"
    )
    rows.append(line())

    for f in fields:
        v1 = str(p1.get(f, ""))
        v2 = str(p2.get(f, ""))
        rows.append(
            f"| {f.ljust(col1_width)} "
            f"| {v1.ljust(col2_width)} "
            f"| {v2.ljust(col3_width)} |"
        )

    rows.append(line())

    compare_table = "\n".join(rows)

    state.response = (
        f"Đây là bảng so sánh thông số giữa {title1} và {title2}:\n"
        f"{compare_table}"
    )

    return state


retrieve_products_chain = RunnableLambda(retrieve_products_docs) | RunnableLambda(build_compare_table)
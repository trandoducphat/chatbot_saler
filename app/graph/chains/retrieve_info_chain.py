import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.retrievers.registry import get_product_retriever
from langchain_core.runnables import RunnableLambda

CAR_FIELDS = {
    "brand": ["hãng", "hãng xe", "thương hiệu", "xe hãng nào", "của hãng nào", "xe của hãng", "hãng sản xuất"],
    "model": ["mẫu", "mẫu xe", "tên xe", "dòng xe", "model", "xe gì", "xe nào", "tên mẫu"],
    "segment": ["phân khúc", "hạng xe", "thuộc phân khúc", "xe hạng", "hạng a", "hạng b", "hạng c", "hạng d"],
    "year": ["năm", "năm sản xuất", "đời", "đời xe", "sản xuất năm", "phiên bản năm", "xe đời bao nhiêu"],
    "price": ["giá", "giá bán", "bao nhiêu tiền", "giá bao nhiêu", "mức giá", "giá lăn bánh", "giá niêm yết", "giá xe", "giá tiền"],
    "body_type": ["kiểu dáng", "dáng xe", "loại xe", "sedan", "suv", "hatchback", "crossover", "mpv", "bán tải"],
    "engine": ["động cơ", "máy", "dung tích", "dung tích động cơ", "bao nhiêu chấm", "1.5", "1.8", "2.0"],
    "fuel": ["nhiên liệu", "xăng", "dầu", "diesel", "hybrid", "điện", "chạy xăng", "chạy dầu"],
    "transmission": ["hộp số", "số sàn", "số tự động", "tự động", "manual", "automatic", "at", "mt"],
    "seats": ["số chỗ", "bao nhiêu chỗ", "mấy chỗ", "5 chỗ", "7 chỗ", "4 chỗ", "ngồi được bao nhiêu người"],
    "origin": ["xuất xứ", "nhập khẩu", "lắp ráp", "sản xuất ở đâu", "xe nhập", "xe lắp ráp", "nước sản xuất", "thái lan", "việt nam", "indonesia"]
}
CAR_FIELD_RENDER = {
    "brand": {
        "label": "Hãng xe",
        "key": "brand"
    },
    "model": {
        "label": "Mẫu xe",
        "key": "model"
    },
    "segment": {
        "label": "Phân khúc",
        "key": "segment"
    },
    "year": {
        "label": "Năm sản xuất",
        "key": "year"
    },
    "price": {
        "label": "Giá bán",
        "key": "price_vnd",
        "format": lambda v: f"{v:,} VNĐ"
    },
    "body_type": {
        "label": "Kiểu dáng",
        "key": "body_type"
    },
    "engine": {
        "label": "Động cơ",
        "key": "engine"
    },
    "fuel": {
        "label": "Nhiên liệu",
        "key": "fuel"
    },
    "transmission": {
        "label": "Hộp số",
        "key": "transmission"
    },
    "seats": {
        "label": "Số chỗ ngồi",
        "key": "seats",
        "format": lambda v: f"{v} chỗ"
    },
    "origin": {
        "label": "Xuất xứ",
        "key": "origin"
    }
}



def retrieve_1_car(user_message: str) -> dict:
    product_retriver = get_product_retriever()
    retrieved_car = product_retriver.retrieve(user_message, 1, 0.3)
    return retrieved_car

def detect_car_fields(user_message: str) -> list[str]:
    detected_fields = []
    for field, keywords in CAR_FIELDS.items():
        for kw in keywords:
            if kw in user_message.lower():
                detected_fields.append(field)
                break
    return detected_fields


def render_car_fields(fields: list[str], car: dict) -> str:
    lines = []

    for field in fields:
        config = CAR_FIELD_RENDER.get(field)
        if not config:
            continue

        key = config["key"]
        value = car.get(key)

        if value is None:
            continue

        if "format" in config:
            value = config["format"](value)

        lines.append(f"- {field}: {value}")

    return "\n".join(lines)

def build_info_answer(state: ChatState) -> ChatState:
    if not state.selected_car:
        retrieved_car = retrieve_1_car(state.user_message)

        if not retrieved_car:
            state.response = "Tôi chưa xác định được sản phẩm mà bạn đang đề cập đến. Hãy mô tả rõ nhất về thông tin (tên hãng + tên mẫu) của sản phẩm."
            return state

        state.selected_car = retrieved_car
    
    fields = detect_car_fields(state.user_message)
    car = state.selected_car

    answer = f"Thông tin mà bạn đang thắc mắc về xe {car[0]['metadata']['brand']} {car[0]['metadata']['model']} đời {car[0]['metadata']['year']} như sau:\n" + render_car_fields(fields, car[0]['metadata'])
    state.response = answer
    return state

retrieve_info_chain = RunnableLambda(build_info_answer)


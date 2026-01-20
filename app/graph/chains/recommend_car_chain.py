import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.retrievers.registry import get_product_retriever
from langchain_core.runnables import RunnableLambda
from app.LLMs.qwen import tokenizer, model
import json
import re
import torch
from app.embeddings.embedding_manager import PROD_DOCS
from typing import Dict, Optional


SCHEMA_KEYS = {
    "brand",
    "model",
    "segment",
    "year",
    "price_vnd",
    "body_type",
    "engine",
    "fuel",
    "transmission",
    "seats",
    "origin",
}


def parse_price_range(message: str) -> Dict[str, Optional[int]]:
    msg = message.lower()

    price_min = None
    price_max = None

    def to_vnd(value: float, unit: str) -> int:
        if unit in ["tỷ", "ty"]:
            return int(value * 1_000_000_000)
        return int(value * 1_000_000)
    
    match = re.search(
        r"(tầm|khoảng|loan quanh|trên dưới)\s+(\d+(?:[.,]\d+)?)\s*(triệu|tr|tỷ|ty)",
        msg
    )
    if match:
        center = to_vnd(float(match.group(2).replace(",", ".")), match.group(3))
        delta = int(center * 0.1)
        return {
            "price_min": center - delta,
            "price_max": center + delta
        }

    match = re.search(
        r"từ\s+(\d+(?:[.,]\d+)?)\s*(triệu|tr|tỷ|ty)\s+đến\s+(\d+(?:[.,]\d+)?)\s*(triệu|tr|tỷ|ty)",
        msg
    )
    if match:
        price_min = to_vnd(float(match.group(1).replace(",", ".")), match.group(2))
        price_max = to_vnd(float(match.group(3).replace(",", ".")), match.group(4))
        return {"price_min": price_min, "price_max": price_max}

    match = re.search(
        r"(dưới|không quá|tối đa)\s+(\d+(?:[.,]\d+)?)\s*(triệu|tr|tỷ|ty)",
        msg
    )
    if match:
        price_max = to_vnd(float(match.group(2).replace(",", ".")), match.group(3))
        return {"price_min": None, "price_max": price_max}

    match = re.search(
        r"(trên|từ)\s+(\d+(?:[.,]\d+)?)\s*(triệu|tr|tỷ|ty)",
        msg
    )
    if match:
        price_min = to_vnd(float(match.group(2).replace(",", ".")), match.group(3))
        return {"price_min": price_min, "price_max": None}

    match = re.search(
        r"(\d+(?:[.,]\d+)?)\s*(triệu|tr|tỷ|ty)",
        msg
    )
    if match:
        center = to_vnd(float(match.group(1).replace(",", ".")), match.group(2))
        delta = int(center * 0.1)
        return {
            "price_min": center - delta,
            "price_max": center + delta
        }

    return {"price_min": None, "price_max": None}


def _clean_json_text(text: str) -> str:
    match = re.search(r"\{.*?\}", text, re.S)
    if not match:
        return ""
    return match.group()


def _normalize_fields(data: dict) -> dict:
    KEY_ALIASES = {
        "segments": "segment",
        "seat": "seats",
        "number_of_seats": "seats",
    }
    normalized = {}

    for k, v in data.items():
        k = KEY_ALIASES.get(k, k)
        if k in SCHEMA_KEYS:
            normalized[k] = v

    if isinstance(normalized.get("segment"), str) and "chỗ" in normalized["segment"]:
        try:
            normalized["seats"] = int(
                re.search(r"\d+", normalized["segment"]).group()
            )
            normalized["segment"] = None
        except Exception:
            pass

    return normalized


def detect_demand(user_message: str) -> dict:
    prompt = f"""
            You are a system for extracting car purchase requirements.

            RULES:
            - Only return valid JSON
            - Do not write code
            - Do not add any text outside the JSON
            - Do not add extra }} Reedundant braces
            - Only use keys defined in the schema

            User message:
            "{user_message}"
            
            Schema:
            {{
              "brand": null,
              "model": null,
              "segment": null,
              "year": null,
              "price_vnd": null,
              "body_type": null,
              "engine": null,
              "fuel": null,
              "transmission": null,
              "seats": null,
              "origin": null
            }}
            
            Only return JSON object.
            Fill by Vietnamese
            """

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=False,
            temperature=0.0,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1,
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    raw = decoded[len(prompt):].strip()

    json_text = _clean_json_text(raw)
    parsed = json.loads(json_text)
    normalized = _normalize_fields(parsed)

    result = {k: normalized.get(k, None) for k in SCHEMA_KEYS}

    return result


def get_fields(fields: dict) -> list:
    filled_fields = [k for k, v in fields.items() if v is not None]
    return filled_fields


def consider_demand_car(demands_fields: list, ideal_car: dict, user_message: str) -> list:
    if len(demands_fields) == 0:
        return None
    
    filted_cars = []
    min_price, max_price = parse_price_range(user_message).values()

    for doc in PROD_DOCS:
        car = doc.__dict__['metadata']
        if not min_price and not max_price:
            filted_cars = [item.__dict__['metadata'] for item in PROD_DOCS]
            break
        
        if min_price and max_price:
            if car.get("price_vnd") >= min_price and car.get("price_vnd") <= max_price:
                filted_cars.append(car)
            elif min_price and not max_price:
                if car.get("price_vnd") >= min_price:
                    filted_cars.append(car)
            elif max_price and not min_price:
                if car.get("price_vnd") <= max_price:
                    filted_cars.append(car)

    new_filted_car = []
    for car in filted_cars:
        flag = True
        for demand in demands_fields:
            demand = demand.lower()
            if demand in ['brand', 'model', 'segment', 'body_type', 'engine', 'fuel', 'transmission', 'origin']:
                car_info = car[demand].lower()
                ideal_info = ideal_car[demand].lower()
                if car_info in ideal_info or ideal_info in car_info:
                    continue
                else:
                    flag = False
                    break
            if demand in ['year', 'seats']:
                car_info = car[demand]
                ideal_info = ideal_car[demand]
                if car_info == ideal_info:
                    continue
                else:
                    flag = False
                    break
        if flag == True:
            new_filted_car.append(car)
    return new_filted_car


def render_table_from_list_dict(items: list[dict]) -> str:
    fields = []
    for item in items:
        for k in item.keys():
            if k not in fields:
                fields.append(k)

    col_widths = {}
    for f in fields:
        max_len = len(f)
        for item in items:
            val = item.get(f, "")
            max_len = max(max_len, len(str(val)))
        col_widths[f] = max_len

    line = "+" + "+".join("-" * (col_widths[f] + 2) for f in fields) + "+"

    rows = []

    rows.append(line)
    rows.append(
        "|" + "|".join(f" {f.ljust(col_widths[f])} " for f in fields) + "|"
    )
    rows.append(line)

    for item in items:
        rows.append(
            "|" + "|".join(
                f" {str(item.get(f, '')).ljust(col_widths[f])} "
                for f in fields
            ) + "|"
        )
    rows.append(line)
    return "\n".join(rows)



def build_recommendation_info(state: ChatState) -> ChatState:
    answer = ""

    ideal_car = detect_demand(state.user_message)
    demands_fields = get_fields(ideal_car)

    filted_car = consider_demand_car(demands_fields, ideal_car, state.user_message)

    if not filted_car:
        answer = "Không có sản phẩm nào phù hợp với yêu cầu bạn đang đề ra."
    #############Có thể retrieve để bổ sung sản phẩm#######################
    else:
        answer = "Dưới đây là những sản phẩm phù hợp với nhu cầu của bạn:\n" + render_table_from_list_dict(filted_car[:5])
    
    if len(filted_car) == 1:
        state.selected_car = filted_car[0]
    elif len(filted_car) == 2:
        state.compared_car = filted_car
    
    state.response = answer
    return state


recommend_car_chain = RunnableLambda(build_recommendation_info)
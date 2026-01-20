import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(root_dir)

from app.graph.state import ChatState
from app.retrievers.registry import get_policy_retriever
from app.config.prompts import POLICY_ANSWER_PROMPT
from app.LLMs.qwen import tokenizer, model
import torch
from langchain_core.runnables import RunnableLambda

def retrieve_policy_docs(state: ChatState) -> ChatState:
    policy_retriever = get_policy_retriever()
    retrieved_policy = policy_retriever.retrieve(state.user_message, 2, 0.3)

    state.retrieved_docs = retrieved_policy
    return state



def build_policy_context(state: ChatState) -> ChatState:
    if not state.retrieved_docs:
        state.policy_context = ""
        return state
    
    blocks = [doc['content'] for doc in state.retrieved_docs]

    state.policy_context = "\n\n---\n\n".join(blocks)
    return state


def generate_policy_answer(state: ChatState) -> ChatState:
    if not state.policy_context:
        state.response = "Xin lỗi, tôi chưa tìm thấy chính sách phù hợp với đề cập của bạn."
        state.history.append(state.response)
        return state
    
    prompt = POLICY_ANSWER_PROMPT.format(
        user_message = state.user_message,
        context = state.policy_context
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=120,
            temperature=None,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = decoded[len(prompt):].strip()

    state.response = answer
    state.history.append(state.response)
    return state


retrieve_policy_chain = RunnableLambda(retrieve_policy_docs) | RunnableLambda(build_policy_context) | RunnableLambda(generate_policy_answer)
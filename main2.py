from app.graph.state import ChatState
from app.graph.graph_builder import build_graph
from app.embeddings.embedding_manager import EmbeddingManager
from app.retrievers.vector_store import VectorStore
from app.retrievers.retriever import RAGRetriever
from app.retrievers.registry import init_retrievers
from app.services.conversation_manager import ConversationManager
from app.bootstrap import init_state, boostrap_chat_app


def main():
    state_id = 0
    boostrap_chat_app()
    graph = build_graph()
    print("=== CHATBOT STARTED ===")
    print("Gõ 'new chat' để tạo cuộc trò chuyện mới")
    print("Gõ 'exit' để thoát")
    print("Gõ 'reset' khởi tạo lại cuộc trò chuyện này")

    sessions = ConversationManager(init_state)
    state = sessions.new_conversation(state_id)
    state_id += 1
    while True:
        user_input = input("Tôi: ")
        if user_input == "exit":
            break

        elif user_input == "new chat":
            state = sessions.new_conversation(state_id)
            state_id += 1
            print("=== Bắt đầu cuộc trò chuyện mới ===")
            continue

        elif user_input == "reset":
            state = sessions.reset(state_id)
            print("===Cuộc trò chuyện đã được khởi tạo lại===")
            continue
        
        else: 
            state['user_message'] = user_input

            state = graph.invoke(state)
            print("Agent: ", state['response'])


if __name__ == "__main__":
    main()
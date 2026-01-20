from langchain_core.documents import Document
import json
from pathlib import Path

class JSONLoader:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
    
    def load(self) -> list[Document]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        documents = []
        for item in data:
            content = item.get("description", "")
            metadata = {k: v for k, v in item.items() if k != "description"}
            documents.append(Document(page_content=content, metadata=metadata))
        
        return documents
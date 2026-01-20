from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
# print(f"Base dir: {BASE_DIR}")

DATA_DIR = BASE_DIR/"data"
EMBEDDINGS_DIR = DATA_DIR/"embeddings"
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
# print(f"Embedding dir: {EMBEDDINGS_DIR}")
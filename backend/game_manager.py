import json
import os

LIBRARY_FILE = "library.json"

def load_library():
    if not os.path.exists(LIBRARY_FILE):
        return []

    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_library(games):
    with open(LIBRARY_FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, indent=4, ensure_ascii=False)

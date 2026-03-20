import json
import os

DB_PATH = "data/attacks.json"

def load_memory():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=2)

def store_attack(prompt, embedding):
    data = load_memory()
    data.append({
        "prompt": prompt,
        "embedding": embedding.tolist()
    })
    save_memory(data)

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from app.embeddings import get_embedding
from app.memory import load_memory

THRESHOLD = 0.85

KEYWORDS = [
    "ignore previous instructions",
    "ignore all previous instructions",
    "reveal system prompt",
    "show system prompt",
    "disregard instructions",
    "bypass safety",
    "act as",
    "you are now"
]

def normalize_prompt(prompt: str):
    return prompt  # 🔥 no LLM here


def detect_attack(prompt: str):
    try:
        normalized = normalize_prompt(prompt)
        lower = normalized.lower()

        # 🔴 Keyword detection
        for k in KEYWORDS:
            if k in lower:
                return {
                    "is_attack": True,
                    "reason": f"keyword_match: {k}",
                    "normalized": normalized
                }

        # 🧠 Embedding detection
        emb = get_embedding(normalized)
        memory = load_memory()

        if len(memory) < 2:
            return {
                "is_attack": False,
                "embedding": emb,
                "normalized": normalized
            }

        for item in memory:
            if item.get("embedding"):
                stored = np.array(item["embedding"])
                sim = cosine_similarity([emb], [stored])[0][0]

                if sim > THRESHOLD and sim < 0.999:
                    return {
                        "is_attack": True,
                        "similarity": float(sim),
                        "normalized": normalized
                    }

        return {
            "is_attack": False,
            "embedding": emb,
            "normalized": normalized
        }

    except Exception as e:
        print("Detection failed:", str(e))
        return {
            "is_attack": False,
            "error": str(e),
            "normalized": prompt
        }
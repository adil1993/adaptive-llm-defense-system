from fastapi import APIRouter
from app.detector import detect_attack
from app.defense import defend
from app.llm import call_llm
from app.memory import store_attack

router = APIRouter()

@router.post("/analyze")
def analyze(prompt: str):
    try:
        detection = detect_attack(prompt)
        decision = defend(prompt, detection)

        # 🚫 BLOCK early (no LLM call)
        if decision["action"] == "block":
            return {
                "status": "blocked",
                "details": detection,
                "normalized": detection.get("normalized")
            }

        # ✅ Only ONE LLM call
        response = call_llm(prompt)

        return {
            "status": "allowed",
            "response": response,
            "normalized": detection.get("normalized")
        }

    except Exception as e:
        print("API error:", str(e))
        return {
            "status": "error",
            "message": str(e)
        }
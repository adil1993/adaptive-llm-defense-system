from fastapi import APIRouter
from app.detector import detect_attack
from app.defense import defend
from app.llm import call_llm
from app.memory import store_attack
from app.evaluator import evaluate_output

router = APIRouter()

@router.post("/analyze")
def analyze(prompt: str):
    try:
        detection = detect_attack(prompt)
        decision = defend(prompt, detection)

        if decision["action"] == "block":
            return {
                "status": "blocked",
                "details": detection,
                "normalized": detection.get("normalized")
            }

        response = call_llm(prompt)
        evaluation = evaluate_output(response)

        if detection.get("embedding") is not None:
            store_attack(prompt, detection["embedding"])

        return {
            "status": "allowed",
            "response": response,
            "evaluation": evaluation,
            "normalized": detection.get("normalized")
        }

    except Exception as e:
        print("API error:", str(e))
        return {"status": "error", "message": str(e)}

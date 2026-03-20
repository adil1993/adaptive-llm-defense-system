def defend(prompt, detection_result):
    if detection_result.get("is_attack") is True:
        return {
            "action": "block",
            "reason": detection_result.get("reason", "attack_detected"),
            "normalized": detection_result.get("normalized")
        }

    return {
        "action": "allow",
        "prompt": prompt,
        "normalized": detection_result.get("normalized")
    }
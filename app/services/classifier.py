def classify_query(query: str) -> dict:
    q = query.lower()

    if "password" in q or "forgot my password" in q or "reset password" in q or "login" in q:
        return {"intent": "technical", "sub_intent": "login", "urgency": "medium", "confidence": 0.95, "entities": [], "sentiment": "neutral"}

    if "charge" in q or "refund" in q or "invoice" in q or "billing" in q or "payment" in q:
        return {"intent": "billing", "sub_intent": "refund" if "refund" in q else None, "urgency": "medium", "confidence": 0.92, "entities": [], "sentiment": "neutral"}

    if "crash" in q or "screen" in q or "network" in q or "laptop" in q:
        return {"intent": "technical", "sub_intent": "app_crash" if "crash" in q else None, "urgency": "medium", "confidence": 0.9, "entities": [], "sentiment": "neutral"}

    return {"intent": "general", "sub_intent": None, "urgency": "low", "confidence": 0.75, "entities": [], "sentiment": "neutral"}
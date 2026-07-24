def resolve_ticket(intent: str, sub_intent: str | None, query: str, context: str) -> str:
    q = query.lower().strip()
    intent = str(intent).lower().strip()
    sub_intent = str(sub_intent).lower().strip() if sub_intent else None

    if "password" in q or "forgot my password" in q or "reset password" in q:
        return "Go to the login page and click Forgot Password. Enter your registered email and use the reset link sent to your inbox."

    if intent == "billing":
        if sub_intent == "refund":
            return "For a refund request, share your order ID and purchase date. Support can verify eligibility and process the refund."
        if "charged twice" in q or "double charge" in q:
            return "Please compare transaction IDs and timestamps. If both charges are valid, contact billing with order ID and payment details."
        return "Please review your billing history and payment details. If needed, contact billing support with the transaction or invoice ID."

    if intent == "technical":
        if sub_intent == "app_crash":
            return "Clear cache, update the app, and reinstall if needed. If it still crashes, send the exact error and device details."
        if "laptop" in q:
            return "Plug in the charger, hold the power button for 10 seconds, and test with an external display."
        return "Try restarting the device, checking updates, and sharing the exact error message."

    if context:
        return context

    return "Thanks for reaching out. Please share a little more detail so I can help."
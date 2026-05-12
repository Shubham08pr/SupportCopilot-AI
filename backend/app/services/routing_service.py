def decide_action(confidence: float):
    """
    Decide what system should do
    based on confidence score
    """

    if confidence >= 0.85:
        return "AUTO_SEND"

    elif confidence >= 0.60:
        return "AGENT_REVIEW"

    else:
        return "ESCALATE"
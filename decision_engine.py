def generate_final_verdict(
    risk_score,
    ai_prediction,
    ai_confidence,
    quantum_probability
):

    final_score = (
        risk_score * 0.5
        + quantum_probability * 0.2
        + ai_confidence * 0.3
    )

    if (
        ai_prediction == "MALICIOUS"
        and ai_confidence >= 70
    ):
        verdict = "HIGH RISK"

    elif final_score >= 70:
        verdict = "HIGH RISK"

    elif final_score >= 40:
        verdict = "MEDIUM RISK"

    else:
        verdict = "SAFE"

    return {
        "final_verdict": verdict,
        "final_score": round(final_score, 2)
    }
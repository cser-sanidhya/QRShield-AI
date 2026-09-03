from merchant_database import KNOWN_MERCHANTS

def calculate_fraud_score(details):

    score = 0
    reasons = []

    upi_id = details.get("upi_id", "").lower()
    merchant = details.get("merchant_name", "")
    amount = details.get("amount", "")

    # Merchant Verification
    if upi_id in KNOWN_MERCHANTS:

        merchant_data = KNOWN_MERCHANTS[upi_id]

        if merchant_data["verified"]:
            score -= 20
            reasons.append("Verified Merchant")

    else:
        score += 30
        reasons.append("Unknown Merchant")

    # Suspicious Keywords
    suspicious_words = [
        "lottery",
        "bonus",
        "reward",
        "prize",
        "win",
        "cashback"
    ]

    text = f"{merchant} {upi_id}".lower()

    for word in suspicious_words:
        if word in text:
            score += 25
            reasons.append(f"Suspicious keyword: {word}")

    # High Amount
    try:
        amt = float(amount)

        if amt > 10000:
            score += 20
            reasons.append("High Amount")

    except:
        pass

    # Final Classification
    if score <= 0:
        risk = "SAFE"

    elif score <= 30:
        risk = "LOW RISK"

    elif score <= 60:
        risk = "MEDIUM RISK"

    else:
        risk = "HIGH RISK"

    return {
        "risk_score": score,
        "risk_level": risk,
        "reasons": reasons
    }
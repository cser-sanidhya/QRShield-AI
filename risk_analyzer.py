import re

from upi_parser import extract_upi_details
from fraud_engine import calculate_fraud_score


SUSPICIOUS_KEYWORDS = [
    "login",
    "signin",
    "verify",
    "verification",
    "secure",
    "security",
    "update",
    "account",
    "wallet",
    "bank",
    "banking",
    "payment",
    "invoice",
    "refund",
    "reward",
    "bonus",
    "prize",
    "lottery",
    "otp",
    "kyc",
    "upi",
    "outlook",
    "microsoft",
    "paypal",
    "amazon",
    "netflix",
    "google",
    "facebook"
]


def analyze_url(qr_text):

    details = extract_upi_details(qr_text)

    fraud_result = calculate_fraud_score(details)

    risk_score = fraud_result["risk_score"]
    reasons = fraud_result["reasons"]

    # Extract URL from dataset text if present
    url_match = re.search(
        r"(https?://[^\s]+)",
        qr_text
    )

    if url_match:
        text = url_match.group(1).lower()
    else:
        text = qr_text.lower()

    # HTTP Detection
    if text.startswith("http://"):

        risk_score += 20

        reasons.append(
            "Uses HTTP instead of HTTPS"
        )

    # IP Address Detection
    ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

    if re.search(ip_pattern, text):

        risk_score += 25

        reasons.append(
            "IP address detected in URL"
        )

    # Long URL Detection
    if len(text) > 100:

        risk_score += 15

        reasons.append(
            "Unusually long URL"
        )

    # Suspicious Keywords
    keyword_count = 0

    for keyword in SUSPICIOUS_KEYWORDS:

        if keyword in text:

            keyword_count += 1

            risk_score += 10

            reasons.append(
                f"Suspicious keyword: {keyword}"
            )

    # Multiple Suspicious Keywords
    if keyword_count >= 3:

        risk_score += 20

        reasons.append(
            "Multiple suspicious keywords detected"
        )

    # Maximum Score
    risk_score = min(risk_score, 100)

    # Risk Classification
    if risk_score >= 70:

        risk_level = "HIGH RISK"

    elif risk_score >= 40:

        risk_level = "MEDIUM RISK"

    else:

        risk_level = "LOW RISK"

    return {
        "upi_details": details,
        "analysis": {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "reasons": reasons
        }
    }
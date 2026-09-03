def detect_upi(qr_text):
    if qr_text.startswith("upi://pay"):
        return {
            "is_upi": True,
            "message": "UPI QR Detected"
        }

    return {
        "is_upi": False,
        "message": "Not a UPI QR"
    }
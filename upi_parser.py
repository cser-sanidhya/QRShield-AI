from urllib.parse import urlparse, parse_qs
import re


def extract_upi_details(qr_text):

    result = {
        "upi_id": "",
        "merchant_name": "",
        "amount": ""
    }

    # Clean dataset artifacts
    qr_text = str(qr_text).strip()

    # Extract actual URL if dataset contains:
    # "416242 http://example.com Name: url, dtype: object"
    url_match = re.search(
        r"(https?://[^\s]+)",
        qr_text
    )

    if url_match:
        qr_text = url_match.group(1)

    # Only process UPI QR codes
    if not qr_text.startswith("upi://"):
        return result

    parsed = urlparse(qr_text)

    params = parse_qs(parsed.query)

    result["upi_id"] = params.get(
        "pa",
        [""]
    )[0]

    result["merchant_name"] = params.get(
        "pn",
        [""]
    )[0]

    result["amount"] = params.get(
        "am",
        [""]
    )[0]

    return result
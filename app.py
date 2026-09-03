from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
from pyzbar.pyzbar import decode
import re

from risk_analyzer import analyze_url
from quantum_optimizer import quantum_risk_optimizer
from qr_predictor import predict_qr
from decision_engine import generate_final_verdict

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QRTextRequest(BaseModel):
    qr_text: str


@app.get("/")
def home():
    return {
        "message": "QRShield AI Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "QRShield AI Backend"
    }


@app.post("/upload_qr")
async def upload_qr(file: UploadFile = File(...)):

    try:

        image = Image.open(file.file)

        ai_result = predict_qr(image)

        decoded_objects = decode(image)

        if len(decoded_objects) == 0:
            return {
                "status": "failed",
                "message": "No QR Code Found",
                "ai_prediction": ai_result
            }

        qr_text = decoded_objects[0].data.decode("utf-8")

        # Clean QR text if dataset added extra values
        url_match = re.search(
            r"https?://[^\s]+",
            qr_text
        )

        if url_match:
            qr_text = url_match.group(0)

        analysis = analyze_url(qr_text)

        risk_score = analysis["analysis"]["risk_score"]

        quantum_result = quantum_risk_optimizer(
            risk_score
        )

        final_result = generate_final_verdict(
            risk_score=risk_score,
            ai_prediction=ai_result["prediction"],
            ai_confidence=ai_result["confidence"],
            quantum_probability=quantum_result["quantum_probability"]
        )

        return {
            "status": "success",
            "qr_data": qr_text,
            "analysis": analysis,
            "quantum_analysis": quantum_result,
            "ai_prediction": ai_result,
            "final_decision": final_result
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/scan_qr_text")
async def scan_qr_text(data: QRTextRequest):

    try:

        qr_text = data.qr_text

        # Clean QR text if URL exists
        url_match = re.search(
            r"https?://[^\s]+",
            qr_text
        )

        if url_match:
            qr_text = url_match.group(0)

        analysis = analyze_url(qr_text)

        risk_score = analysis["analysis"]["risk_score"]

        quantum_result = quantum_risk_optimizer(
            risk_score
        )

        final_result = generate_final_verdict(
            risk_score=risk_score,
            ai_prediction="BENIGN",
            ai_confidence=50,
            quantum_probability=quantum_result["quantum_probability"]
        )

        return {
            "status": "success",
            "qr_data": qr_text,
            "analysis": analysis,
            "quantum_analysis": quantum_result,
            "final_decision": final_result
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI(title="DevOps AI Platform")

REQUEST_COUNT = Counter(
    "inference_requests_total",
    "Total inference requests"
)

class PredictionRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {
        "message": "DevOps AI Platform Running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    REQUEST_COUNT.inc()

    text = request.text.lower()

    positive_words = [
        "good",
        "great",
        "awesome",
        "love",
        "excellent",
        "happy"
    ]

    negative_words = [
        "bad",
        "terrible",
        "hate",
        "awful",
        "sad"
    ]

    positive_score = sum(
        word in text for word in positive_words
    )

    negative_score = sum(
        word in text for word in negative_words
    )

    sentiment = (
        "positive"
        if positive_score >= negative_score
        else "negative"
    )

    return {
        "sentiment": sentiment
    }

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )
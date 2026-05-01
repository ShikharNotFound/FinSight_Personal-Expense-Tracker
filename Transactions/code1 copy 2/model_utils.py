from __future__ import annotations

import os
import re
from pathlib import Path

import joblib

BASE_DIR = Path(__file__).resolve().parent

# Prefer requested file name, but support the existing file in this workspace.
CANDIDATE_MODELS = [
    BASE_DIR / "expense_classifier.pkl",
    BASE_DIR / "expense_classifier (1).pkl",
]

MODEL_PATH = next((path for path in CANDIDATE_MODELS if path.exists()), None)
model = None

if MODEL_PATH is not None:
    # Safety check: ensure resolved model path remains inside project directory.
    resolved_base = BASE_DIR.resolve()
    resolved_model = MODEL_PATH.resolve()
    if resolved_base not in resolved_model.parents and resolved_model != resolved_base:
        raise RuntimeError("Unsafe model path detected")

    model = joblib.load(str(resolved_model))


KEYWORD_CATEGORIES = [
    ("Food", r"\b(food|restaurant|cafe|coffee|swiggy|zomato|pizza|burger|meal|grocery|grocer)\b"),
    ("Shopping", r"\b(amazon|flipkart|myntra|shopping|store|mall|purchase)\b"),
    ("Travel", r"\b(uber|ola|metro|fuel|petrol|diesel|flight|train|bus|hotel|travel)\b"),
    ("Utilities", r"\b(electricity|water|gas|wifi|broadband|mobile|recharge|bill)\b"),
    ("Healthcare", r"\b(pharmacy|hospital|doctor|clinic|medical|health)\b"),
    ("Education", r"\b(course|school|college|tuition|book|exam|education)\b"),
    ("Investment", r"\b(sip|mutual|fund|stock|zerodha|groww|investment)\b"),
    ("EMI", r"\b(emi|loan|interest|repayment)\b"),
    ("Entertainment", r"\b(netflix|spotify|movie|cinema|game|entertainment)\b"),
]


def _keyword_predict(description: str) -> dict:
    text = description.lower()
    for category, pattern in KEYWORD_CATEGORIES:
        if re.search(pattern, text):
            return {"category": category, "confidence": 0.65}
    return {"category": "Other", "confidence": 0.4}


def predict_transaction(description: str) -> dict:
    if model is None:
        return _keyword_predict(description)

    prediction = model.predict([description])[0]

    confidence = None
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba([description])[0]
        confidence = float(max(probs))

    return {
        "category": str(prediction),
        "confidence": round(confidence, 3) if confidence is not None else None,
    }

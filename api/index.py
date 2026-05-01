from datetime import date, datetime

import jwt
from bson import ObjectId
from flask import jsonify, request
from pymongo import errors

from backend.auth_server import JWT_ALGORITHM, JWT_SECRET, app as flask_app, db
from backend.ChatBot import local_finance_reply


transactions_collection = db["transactions"]


def _current_user_id():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None, ("Missing bearer token", 401)

    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
    except jwt.PyJWTError:
        return None, ("Invalid or expired token", 401)

    if not user_id:
        return None, ("Invalid token payload", 401)
    return user_id, None


def _json_safe(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, dict):
        return {key: _json_safe(item) for key, item in value.items()}
    return value


def _normalize_transaction(doc):
    payload = _json_safe(doc)
    payload["id"] = payload.get("id") or payload.get("_id")
    payload["description"] = payload.get("description") or payload.get("merchant") or ""
    payload["category"] = payload.get("category") or payload.get("cat") or "Other"
    return payload


@flask_app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", "")).strip()

    if not user_message:
        return jsonify({"reply": "Please enter a message so I can help."}), 400

    return jsonify({"reply": local_finance_reply(user_message), "source": "local_fallback"})


@flask_app.get("/transactions")
@flask_app.get("/ledger")
def list_transactions():
    user_id, auth_error = _current_user_id()
    if auth_error:
        message, status = auth_error
        return jsonify({"detail": message}), status

    query = {"user_id": user_id}
    try:
        user_oid = ObjectId(user_id)
        query = {"$or": [{"user_id": user_id}, {"user_id": user_oid}]}
    except Exception:
        pass

    try:
        docs = list(transactions_collection.find(query).sort("date", -1).limit(500))
    except errors.PyMongoError as exc:
        return jsonify({"detail": f"Database error while fetching transactions: {exc}"}), 500

    return jsonify({"transactions": [_normalize_transaction(doc) for doc in docs]})


class StripApiPrefix:
    def __init__(self, wrapped_app):
        self.wrapped_app = wrapped_app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO", "")
        if path == "/api":
            environ["PATH_INFO"] = "/"
        elif path.startswith("/api/"):
            environ["PATH_INFO"] = path[4:]
        return self.wrapped_app(environ, start_response)


app = StripApiPrefix(flask_app)

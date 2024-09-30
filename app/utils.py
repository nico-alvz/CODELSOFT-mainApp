import time
from functools import wraps
import jwt
import requests
from flask import request, jsonify
from .config import Config

def call_service_with_retries(url, method, payload=None, headers=None, params=None):
    retries = 0
    delay = Config.BASE_DELAY

    while retries < Config.MAX_RETRIES:
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=payload, headers=headers, timeout=10)
            elif method.upper() == "PUT":
                response = requests.put(url, json=payload, headers=headers, timeout=10)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=headers, params=params, timeout=10)
            else:
                raise ValueError("Unsupported HTTP method")

            if 200 <= response.status_code < 300:
                return response.json()
            else:
                raise Exception(f"Service returned error: {response.status_code} - {response.text}")
        except Exception as e:
            retries += 1
            print(f"Error calling service. Attempt {retries}/{Config.MAX_RETRIES}: {e}")
            time.sleep(delay)
            delay *= 2

    raise Exception("Failed to call service after multiple attempts")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split()
            if len(parts) == 2 and parts[0] == "Bearer":
                token = parts[1]
        if not token:
            return jsonify({"error": "Authorization token is missing"}), 401
        try:
            data = jwt.decode(token, Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM])
            request.user = data
        except Exception:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)
    return decorated

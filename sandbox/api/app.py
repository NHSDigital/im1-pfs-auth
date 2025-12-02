from flask import Flask, Response

from .authentication import post_authenticate

app = Flask(__name__)


@app.route("/_status", methods=["GET"])
@app.route("/_ping", methods=["GET"])
@app.route("/health", methods=["GET"])
def health() -> dict:
    """Health check endpoint."""
    return {
        "status": "online",
        "message": "IM1 PFS Auth API Sandbox is running",
    }


@app.route("/authenticate", methods=["POST"])
def authenticate() -> Response:
    """Sandbox API for POST /authenticate.

    Returns:
        Response: Response for POST /authenticate
    """
    return post_authenticate()

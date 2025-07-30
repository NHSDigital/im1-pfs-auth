from flask import Flask, Response
from .authentication import post_authentication

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello_world():
    return "<p>Welcome to the IM1 PFS Auth Sandbox</p>"


@app.route("/_status", methods=["GET"])
@app.route("/_ping", methods=["GET"])
@app.route("/health", methods=["GET"])
def health() -> dict:
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "IM1 PFS Auth API Sandbox is running",
    }


@app.route("/authentication", methods=["POST"])
def authentication() -> Response:
    """Sandbox API for POST /authentication

    Returns:
        Response: Response for POST /authentication
    """
    return post_authentication()

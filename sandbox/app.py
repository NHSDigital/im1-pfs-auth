from flask import Flask, Response
from .authentication import post_authentication

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome to the IM1 PFS Auth Sandbox</p>"

@app.route("/authentication", methods = [""])
def authentication() -> Response:
    """Sandbox API for POST /authentication
    
    Returns:
        Response: Response for POST /authentication
    """
    post_authentication()
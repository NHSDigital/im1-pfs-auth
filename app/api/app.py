from os import getenv

from flask import Flask, Response, jsonify, make_response

app = Flask(__name__)


@app.route("/authentication", methods=["POST"])
def authentication() -> Response:
    """Application API for POST /authentication.

    Returns:
        Response: Response for POST /authentication
    """
    try:
        getenv("AUTHENTICATION_API_KEY")  # Useless call to test the exception handling
        return make_response(
            jsonify(message="Hello from the IM1 PFS Auth API!", hello="world"), 200
        )

    except Exception as e:
        app.logger.exception("Error in POST /authentication")
        return make_response(jsonify(error=f"Exception: {type(e).__name__}"), 500)

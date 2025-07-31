from json import dumps
from os import getenv

from flask import Flask, Response

app = Flask(__name__)


@app.route("/authentication", methods=["POST"])
def authentication() -> Response:
    """Application API for POST /authentication.

    Returns:
        Response: Response for POST /authentication
    """
    try:
        getenv("AUTHENTICATION_API_KEY")  # Useless call to test the exception handling
        return Response(
            dumps({"message": "Hello from the IM1 PFS Auth API!", "hello": "world"}),
            status=200,
        )

    except Exception as e:
        app.logger.exception("Error in POST /authentication")
        return Response(
            dumps({"error": type(e).__name__}), status=500
        )  # Temporarily return error name

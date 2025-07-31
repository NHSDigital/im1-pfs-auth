from flask import Flask, Response

app = Flask(__name__)


@app.route("/authentication", methods=["POST"])
def authentication() -> Response:
    """Application API for POST /authentication.

    Returns:
        Response: Response for POST /authentication
    """
    try:
        return Response(
            {"message": "Hello from the IM1 PFS Auth API!", "hello": "world"},
            status=200,
        )

    except Exception as e:  # noqa: BLE001 : Catch all exceptions in Application API
        return Response({"error": f"An error occurred: {e!s}"}, status=500)

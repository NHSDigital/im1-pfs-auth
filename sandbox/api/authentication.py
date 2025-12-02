from flask import Response, jsonify, make_response, request


def post_authenticate() -> Response:
    """Sandbox API for POST /authenticate.

    Returns:
        Response: Response for POST /authenticate
    """
    # Get request body
    forward_to = request.headers.get("X-Forward-To")
    ods_code = request.headers.get("X-ODS-Code")
    if forward_to == "https://example.com" and ods_code == "A29929":
        # Successful Request
        data = {
            "sessionId": "123",
            "supplier": "TPP",
            "proxy": {"first_name": "Sarah", "surname": "Jones", "title": "Ms"},
            "patients": [{"first_name": "James", "surname": "Jones", "title": "Mr"}],
        }
        return make_response(jsonify(data), 201)
    # Failure
    data = {"message": "Invalid scenario"}
    return make_response(jsonify(data), 500)

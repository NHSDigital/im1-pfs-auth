from flask import jsonify, make_response, Response, request

def post_authentication() -> Response:
    """Sandbox API for POST /authentication
    
    Returns:
        Response: Response for POST /authentication
    """
    # Get request body
    forward_to = request.headers.get("X-Forward-To")
    ods_code = request.headers.get("X-ODS-Code")
    if forward_to == "https://example.com" and ods_code == "A29929":
        # Successful Request
        data = {
            "sessionId": "123",
            "userPatientLinkToken": "123",
            "suid": "123",
            "onlineUserId": "123",
            "patientId": "123",
        }
        return make_response(jsonify(data), 201)
    else:
        # Failure
        data = {
            "message": "Invalid scenario"
        }
        return make_response(jsonify(data), 500)
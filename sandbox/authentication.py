from flask import Response, request

def post_authentication() -> Response:
    """Sandbox API for POST /authentication
    
    Returns:
        Response: Response for POST /authentication
    """
    # Get request body
    request_body = request.get_json()
    return request_body
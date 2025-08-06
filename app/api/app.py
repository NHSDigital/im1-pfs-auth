from flask import Flask, Response, jsonify, make_response
from http import HTTPStatus

from .exception import ApiException
from .utils import (
    validate_correlation_id,
    validate_forward_to,
    validate_nhs_number,
    validate_ods_code,
    validate_proofing_level,
    validate_request_id,
    validate_vot_level,
)

app = Flask(__name__)


@app.route("/authentication", methods=["POST"])
def authentication() -> Response:
    """Application API for POST /authentication.

    Returns:
        Response: Response for POST /authentication
    """
    try:
        for func in [
            validate_nhs_number,
            validate_proofing_level,
            validate_vot_level,
            validate_ods_code,
            validate_request_id,
            validate_correlation_id,
            validate_forward_to,
        ]:
            func()
        return make_response(
            jsonify(message="Hello from the IM1 PFS Auth API!", hello="world"),
            HTTPStatus.OK,
        )
    except ApiException as e:
        return make_response(jsonify(message=e.message), e.status_code)
    except Exception as e:
        app.logger.exception("Error in POST /authentication")
        return make_response(
            jsonify(error=f"Exception: {type(e).__name__}"),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

from flask import Flask, Response, jsonify, make_response, request
from http import HTTPStatus

from .domain.exception import ApiException
from .domain.forward_request_model import ForwardRequest
from .application.forward_request import route_and_forward

app = Flask(__name__)


@app.route("/authentication", methods=["POST"])
def authentication() -> Response:
    """Application API for POST /authentication.

    Returns:
        Response: Response for POST /authentication
    """
    try:
        forward_request = ForwardRequest(
            application_id=request.headers.get("X-Application-ID"),
            forward_to=request.headers.get("X-Forward-To"),
            patient_nhs_number=request.headers.get(
                "NHSD-NHSlogin-NHS-Number"
            ),  # TODO: Needs updating
            patient_ods_code=request.headers.get("X-ODS-Code"),
            proxy_nhs_number=request.headers.get("NHSD-NHSlogin-NHS-Number"),
        )
        response = route_and_forward(forward_request)
        return make_response(
            jsonify(response.dict()),
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

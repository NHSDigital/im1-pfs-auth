from http import HTTPStatus

from flask import Flask, Response, jsonify, make_response, request

from .application.forward_request import route_and_forward
from .application.jwt import get_nhs_number_from_jwt_token
from .domain.exception import ApiError
from .domain.forward_request_model import ForwardRequest

app = Flask(__name__)


@app.route("/authentication", methods=["POST"])
def authentication() -> Response:
    """Application API for POST /authentication.

    Returns:
        Response: Response for POST /authentication
    """
    try:
        (patient_nhs_number, proxy_nhs_number) = get_nhs_number_from_jwt_token(
            request.headers.get("X-ID-Token")
        )
        forward_request = ForwardRequest(
            application_id=request.headers.get("X-Application-ID"),
            forward_to=request.headers.get("X-Forward-To"),
            patient_nhs_number=patient_nhs_number,
            patient_ods_code=request.headers.get("X-ODS-Code"),
            proxy_nhs_number=proxy_nhs_number,
        )
        response = route_and_forward(forward_request)
        return make_response(
            jsonify(response.model_dump(by_alias=True)),
            HTTPStatus.CREATED,
        )
    except ApiError as e:
        return make_response(jsonify(message=e.message), e.status_code)
    except Exception as e:
        app.logger.exception("Error in POST /authentication")
        return make_response(
            jsonify(error=f"Exception: {type(e).__name__}"),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

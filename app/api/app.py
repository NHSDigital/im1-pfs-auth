from http import HTTPStatus

from flask import Flask, Response, jsonify, make_response, request

from .application.forward_request import route_and_forward
from .application.jwt import get_nhs_number_from_jwt_token
from .domain.exception import ApiError
from .domain.forward_request_model import ForwardRequest

app = Flask(__name__)


@app.route("/authenticate", methods=["POST"])
def authenticate() -> Response:
    """Application API for POST /authenticate.

    Returns:
        Response: Response for POST /authenticate
    """
    try:
        (patient_nhs_number, proxy_nhs_number) = get_nhs_number_from_jwt_token(
            request.headers.get("NHSE-ID-Token")
        )
        forward_request = ForwardRequest(
            application_id=request.headers.get("NHSE-Application-ID"),
            forward_to=request.headers.get("NHSE-Forward-To"),
            patient_nhs_number=patient_nhs_number,
            patient_ods_code=request.headers.get("NHSE-ODS-Code"),
            proxy_nhs_number=proxy_nhs_number,
            use_mock=request.headers.get("NHSE-Use-Mock") == "True",
        )
        response = route_and_forward(forward_request)
        return make_response(
            response.model_dump_json(by_alias=True),
            HTTPStatus.CREATED,
        )
    except ApiError as e:
        return make_response(jsonify(message=e.message), e.status_code)
    except Exception as e:
        app.logger.exception("Error in POST /authenticate")
        return make_response(
            jsonify(error=f"Exception: {type(e).__name__}"),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

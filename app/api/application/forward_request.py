from os import environ

from app.api.domain.exception import ApiError, DownstreamError, InvalidValueError
from app.api.domain.forward_request_model import ForwardRequest
from app.api.domain.forward_response_model import ForwardResponse
from app.api.infrastructure.emis.client import EmisClient
from app.api.infrastructure.tpp.client import TPPClient

EMIS_BASE_URL = environ.get("EMIS_BASE_URL")
TPP_BASE_URL = environ.get("TPP_BASE_URL")
CLIENT_MAP = {EMIS_BASE_URL: EmisClient, TPP_BASE_URL: TPPClient}


def route_and_forward(forward_request: ForwardRequest) -> ForwardResponse:
    """Responsible for routing incoming requests to the appropriate backend client.

    Args:
        forward_request: Class containing details of the forwarding request
    Returns:
        ForwardResponse: Transformed response from client
    """
    try:
        client = CLIENT_MAP[forward_request.forward_to](forward_request)
        response = client.forward_request()
        return client.transform_response(response)
    except KeyError as exc:
        msg = "Invalid URL"
        raise InvalidValueError(msg) from exc
    except ApiError:
        raise
    except Exception as exc:
        msg = "Error occurred with downstream service"
        raise DownstreamError(msg) from exc

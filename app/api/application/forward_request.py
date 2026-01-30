from os import environ

from app.api.domain.exception import ApiError, DownstreamError, InvalidValueError
from app.api.domain.forward_request_model import ForwardRequest
from app.api.domain.forward_response_model import ForwardResponse
from app.api.infrastructure.emis.client import EmisClient
from app.api.infrastructure.tpp.client import TPPClient

ENVIRONMENT = environ.get("ENVIRONMENT", "")
EMIS_URL = (
    "https://api.pfs.emis-x.uk"
    if ENVIRONMENT == "prod"
    else "https://nhs70apptest.emishealth.com"
)
TPP_URL = (
    "https://systmonline.tpp-uk.com"
    if ENVIRONMENT == "prod"
    else "https://systmonline2.tpp-uk.com"
)
CLIENT_MAP = {EMIS_URL: EmisClient, TPP_URL: TPPClient}


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

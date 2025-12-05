from ..domain.exception import ApiError, DownstreamError
from ..domain.forward_request_model import ForwardRequest
from ..domain.forward_response_model import ForwardResponse
from ..infrastructure.emis.client import EmisClient
from ..infrastructure.tpp.client import TPPClient

client_map = {"https://emis.com": EmisClient, "https://tpp.com": TPPClient}


def route_and_forward(forward_request: ForwardRequest) -> ForwardResponse:
    """Responsible for routing incoming requests to the appropriate backend client.

    Args:
        forward_request: Class containing details of the forwarding request
    Returns:
        ForwardResponse: Transformed response from client
    """
    try:
        client = client_map[forward_request.forward_to](forward_request)
        response = client.forward_request()
        return client.transform_response(response)
    except ApiError:
        raise
    except Exception as exc:
        msg = "Error occurred with downstream service"
        raise DownstreamError(msg) from exc

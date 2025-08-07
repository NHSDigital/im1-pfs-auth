from domain.forward_request_model import ForwardRequest
from domain.forward_response_model import ForwardResponse
from infrastructure.emis_client import EmisClient
from infrastructure.tpp_client import TppClient

client_map = {"https://emis.com": EmisClient, "https://tpp.com": TppClient}


def route_and_forward(forward_request: ForwardRequest) -> ForwardResponse:
    """Responsible for routing incoming requests to the appropriate backend client

    Args:
        forward_request: Class containing details of the forwarding request
    Returns:
        ForwardResponse: Transformed response from client
    """
    client = client_map[forward_request.forward_to](forward_request)
    response = client.forward_request()
    return client.transform_response(response)

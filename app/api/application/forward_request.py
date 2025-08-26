from ..domain.exception import DownstreamError
from ..domain.forward_request_model import ForwardRequest
from ..domain.forward_response_model import ForwardResponse
from ..infrastructure.emis_client import EmisClient

client_map = {
    "https://emis.com": EmisClient
}  # TODO(NPA-5401): Add TPP Client and change URL - https://nhsd-jira.digital.nhs.uk/browse/NPA-5401  # noqa: E501, FIX002


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
    except Exception as exc:
        msg = "Error occurred with downstream service"
        raise DownstreamError(msg) from exc

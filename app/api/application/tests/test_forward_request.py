from unittest.mock import MagicMock

import pytest

from app.api.application import forward_request as forward_request_module
from app.api.application.forward_request import route_and_forward
from app.api.domain.exception import DownstreamError, ForbiddenError
from app.api.domain.forward_request_model import ForwardRequest


def test_route_and_forward() -> None:
    """Tests the route_and_forward function."""
    # Arrange
    forward_request = ForwardRequest(
        application_id="some application",
        forward_to="https://example.com",
        patient_nhs_number="1234567890",
        patient_ods_code="some ods code",
        proxy_nhs_number="0987654321",
    )
    mock_client = MagicMock()
    mock_client.return_value.transform_response.return_value = (
        "mocked transformed response"
    )
    forward_request_module.client_map["https://example.com"] = mock_client
    # Act
    actual_result = route_and_forward(forward_request)

    # Assert
    assert actual_result == "mocked transformed response"


def test_route_and_forward_raises_api_error() -> None:
    """Tests the route_and_forward function raises api error."""
    # Arrange
    forward_request = ForwardRequest(
        application_id="some application",
        forward_to="https://example.com",
        patient_nhs_number="1234567890",
        patient_ods_code="some ods code",
        proxy_nhs_number="0987654321",
    )
    mock_client = MagicMock()
    mock_client.return_value.forward_request.side_effect = ForbiddenError("Oops")
    forward_request_module.client_map["https://example.com"] = mock_client
    # Act & Assert
    with pytest.raises(ForbiddenError, match="Oops"):
        route_and_forward(forward_request)


def test_route_and_forward_raises_downstream_error() -> None:
    """Tests the route_and_forward function raises downstream error."""
    # Arrange
    forward_request = ForwardRequest(
        application_id="some application",
        forward_to="https://example.com",
        patient_nhs_number="1234567890",
        patient_ods_code="some ods code",
        proxy_nhs_number="0987654321",
    )
    mock_client = MagicMock()
    mock_client.return_value.forward_request.side_effect = Exception("Oops")
    forward_request_module.client_map["https://example.com"] = mock_client
    # Act & Assert
    with pytest.raises(DownstreamError, match="Error occurred with downstream service"):
        route_and_forward(forward_request)

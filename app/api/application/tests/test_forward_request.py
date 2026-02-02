from importlib import reload
from unittest.mock import patch

import pytest

from app.api.domain.exception import DownstreamError, ForbiddenError, InvalidValueError
from app.api.domain.forward_request_model import ForwardRequest

FILE_PATH = "app.api.application.forward_request"


def test_route_and_forward_emis() -> None:
    """Tests the route_and_forward function."""
    # Arrange
    forward_request = ForwardRequest(
        application_id="some application",
        forward_to="https://emis.com",
        patient_nhs_number="1234567890",
        patient_ods_code="some ods code",
        proxy_nhs_number="0987654321",
        use_mock=False,
    )

    with (
        patch.dict("os.environ", {"EMIS_BASE_URL": "https://emis.com"}),
        patch("app.api.infrastructure.emis.client.EmisClient") as mock_emis_client,
        patch("app.api.infrastructure.tpp.client.TPPClient") as mock_tpp_client,
    ):
        from app.api.application import (
            forward_request as forward_request_module,
        )

        mock_emis_client.return_value.transform_response.return_value = (
            "mocked transformed response"
        )

        reload(forward_request_module)

        # Act
        actual_result = forward_request_module.route_and_forward(forward_request)

        # Assert
        assert actual_result == "mocked transformed response"
        mock_emis_client.return_value.forward_request.assert_called_once()
        mock_emis_client.return_value.transform_response.assert_called_once()
        mock_tpp_client.assert_not_called()


def test_route_and_forward_tpp() -> None:
    """Tests the route_and_forward function."""
    # Arrange
    forward_request = ForwardRequest(
        application_id="some application",
        forward_to="https://tpp.com",
        patient_nhs_number="1234567890",
        patient_ods_code="some ods code",
        proxy_nhs_number="0987654321",
        use_mock=False,
    )

    with (
        patch.dict("os.environ", {"TPP_BASE_URL": "https://tpp.com"}),
        patch("app.api.infrastructure.emis.client.EmisClient") as mock_emis_client,
        patch("app.api.infrastructure.tpp.client.TPPClient") as mock_tpp_client,
    ):
        from app.api.application import (
            forward_request as forward_request_module,
        )

        mock_tpp_client.return_value.transform_response.return_value = (
            "mocked transformed response"
        )

        reload(forward_request_module)

        # Act
        actual_result = forward_request_module.route_and_forward(forward_request)

        # Assert
        assert actual_result == "mocked transformed response"
        mock_emis_client.assert_not_called()
        mock_tpp_client.return_value.forward_request.assert_called_once()
        mock_tpp_client.return_value.transform_response.assert_called_once()


def test_route_and_forward_invalid_url() -> None:
    """Tests the route_and_forward function."""
    # Arrange
    forward_request = ForwardRequest(
        application_id="some application",
        forward_to="https://example.com",
        patient_nhs_number="1234567890",
        patient_ods_code="some ods code",
        proxy_nhs_number="0987654321",
        use_mock=False,
    )

    with (
        patch.dict(
            "os.environ",
            {"EMIS_BASE_URL": "https://emis.com", "TPP_BASE_URL": "https://tpp.com"},
        ),
        patch("app.api.infrastructure.emis.client.EmisClient") as mock_emis_client,
        patch("app.api.infrastructure.tpp.client.TPPClient") as mock_tpp_client,
    ):
        from app.api.application import (
            forward_request as forward_request_module,
        )

        reload(forward_request_module)

        # Act & Assert
        with pytest.raises(InvalidValueError, match="Invalid URL"):
            forward_request_module.route_and_forward(forward_request)
        mock_emis_client.assert_not_called()
        mock_tpp_client.assert_not_called()


def test_route_and_forward_raises_api_error() -> None:
    """Tests the route_and_forward function raises api error."""
    # Arrange
    forward_request = ForwardRequest(
        application_id="some application",
        forward_to="https://emis.com",
        patient_nhs_number="1234567890",
        patient_ods_code="some ods code",
        proxy_nhs_number="0987654321",
        use_mock=False,
    )
    with (
        patch.dict(
            "os.environ",
            {"EMIS_BASE_URL": "https://emis.com", "TPP_BASE_URL": "https://tpp.com"},
        ),
        patch("app.api.infrastructure.emis.client.EmisClient") as mock_emis_client,
    ):
        from app.api.application import forward_request as forward_request_module

        mock_emis_client.return_value.forward_request.side_effect = ForbiddenError(
            "Oops"
        )

        reload(forward_request_module)

        # Act & Assert
        with pytest.raises(ForbiddenError, match="Oops"):
            forward_request_module.route_and_forward(forward_request)


def test_route_and_forward_raises_downstream_error() -> None:
    """Tests the route_and_forward function raises downstream error."""
    # Arrange
    forward_request = ForwardRequest(
        application_id="some application",
        forward_to="https://emis.com",
        patient_nhs_number="1234567890",
        patient_ods_code="some ods code",
        proxy_nhs_number="0987654321",
        use_mock=False,
    )
    with (
        patch.dict(
            "os.environ",
            {"EMIS_BASE_URL": "https://emis.com", "TPP_BASE_URL": "https://tpp.com"},
        ),
        patch("app.api.infrastructure.emis.client.EmisClient") as mock_emis_client,
    ):
        from app.api.application import forward_request as forward_request_module

        mock_emis_client.return_value.forward_request.side_effect = Exception("Oops")

        reload(forward_request_module)

        # Act & Assert
        with pytest.raises(
            DownstreamError, match="Error occurred with downstream service"
        ):
            forward_request_module.route_and_forward(forward_request)

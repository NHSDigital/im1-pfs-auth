import pytest

from app.api.domain.exception import (
    AccessDeniedError,
    InvalidValueError,
    MissingValueError,
)
from app.api.domain.forward_request_model import ForwardRequest


def test_forward_request() -> None:
    """Tests the ForwardRequest model."""
    # Act & Assert
    ForwardRequest(
        application_id="some application",
        forward_to="https://example.com",
        patient_nhs_number="some nhs number",
        patient_ods_code="some ods code",
        proxy_nhs_number="some other nhs number",
    )


@pytest.mark.parametrize(
    ("application_id", "ods_code", "forward_to"),
    [
        (None, "ods code", "https://example.com"),
        ("", "ods code", "https://example.com"),
        ("application id", None, "https://example.com"),
        ("application id", "", "https://example.com"),
        ("application id", "ods code", None),
        ("application id", "ods code", ""),
    ],
)
def test_forward_request_validates_required_field(
    application_id: str, ods_code: str, forward_to: str
) -> None:
    """Tests the ForwardRequest model validates required fields."""
    # Act & Assert
    with pytest.raises(MissingValueError, match="Missing required value"):
        ForwardRequest(
            application_id=application_id,
            forward_to=forward_to,
            patient_nhs_number="some nhs number",
            patient_ods_code=ods_code,
            proxy_nhs_number="some other nhs number",
        )


@pytest.mark.parametrize(
    ("patient_nhs_number", "proxy_nhs_number"),
    [
        (None, "some nhs number"),
        ("", "some nhs number"),
        ("some nhs number", None),
        ("some nhs number", ""),
        (None, None),
        ("", ""),
    ],
)
def test_forward_request_validates_nhs_numbers(
    patient_nhs_number: str, proxy_nhs_number: str
) -> None:
    """Tests the ForwardRequest model validates forward to is a url."""
    # Act & Assert
    with pytest.raises(AccessDeniedError, match="Failed to retrieve NHS Number"):
        ForwardRequest(
            application_id="some application",
            forward_to="https://example.com",
            patient_nhs_number=patient_nhs_number,
            patient_ods_code="some ods code",
            proxy_nhs_number=proxy_nhs_number,
        )


def test_forward_request_validates_forward_to() -> None:
    """Tests the ForwardRequest model validates forward to is a url."""
    # Arrange
    forward_to = "some random value"
    # Act & Assert
    with pytest.raises(InvalidValueError, match="Invalid url"):
        ForwardRequest(
            application_id="some application",
            forward_to=forward_to,
            patient_nhs_number="some nhs number",
            patient_ods_code="some ods code",
            proxy_nhs_number="some other nhs number",
        )

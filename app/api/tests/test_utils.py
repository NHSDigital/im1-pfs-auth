from flask import Flask
from uuid import uuid4

import pytest

from app.api.exception import AccessDenied, ApiException, InvalidValue, MissingValue
from app.api.utils import (
    validate_correlation_id,
    validate_forward_to,
    validate_nhs_number,
    validate_ods_code,
    validate_proofing_level,
    validate_request_id,
    validate_vot_level,
)

app = Flask(__name__)  # Create a Flask app for testing


def test_validate_nhs_number() -> None:
    """Test the validate_nhs_number func."""
    # Arrange
    with app.test_request_context(headers={"NHSD-NHSlogin-NHS-Number": "1234567890"}):
        # Act & Assert
        validate_nhs_number()


@pytest.mark.parametrize("headers", [{"NHSD-NHSlogin-NHS-Number": ""}, {}])
def test_validate_nhs_number_access_denied_exception(headers: dict) -> None:
    """Test the validate_nhs_number func when missing required header."""
    # Arrange
    with app.test_request_context(headers=headers):
        # Act & Assert
        with pytest.raises(
            AccessDenied, match="Failed to retrieve NHS Number for logged in user"
        ):
            validate_nhs_number()


def test_validate_proofing_level() -> None:
    """Test the validate_proofing_level func."""
    # Arrange
    with app.test_request_context(
        headers={"NHSD-NHSlogin-Identity-Proofing-Level": "P9"}
    ):
        # Act & Assert
        validate_proofing_level()


@pytest.mark.parametrize(
    "headers, exception_message",
    [
        ({"NHSD-NHSlogin-Identity-Proofing-Level": "P5"}, "Incorrect proofing level"),
        ({"NHSD-NHSlogin-Identity-Proofing-Level": "P0"}, "Incorrect proofing level"),
        (
            {"NHSD-NHSlogin-Identity-Proofing-Level": "Something random"},
            "Incorrect proofing level",
        ),
        (
            {"NHSD-NHSlogin-Identity-Proofing-Level": ""},
            "Failed to retrieve proofing level for logged in user",
        ),
        ({}, "Failed to retrieve proofing level for logged in user"),
    ],
)
def test_validate_proofing_level_access_denied_exception(
    headers: dict, exception_message: str
) -> None:
    """Test the validate_proofing_level func when invalid required header."""
    # Arrange
    with app.test_request_context(headers=headers):
        # Act & Assert
        with pytest.raises(AccessDenied, match=exception_message):
            validate_proofing_level()


def test_validate_vot_level() -> None:
    """Test the validate_vot_level func."""
    # Arrange
    with app.test_request_context(headers={"NHSD-ID-Token": "P9"}):
        # Act & Assert
        validate_vot_level()


@pytest.mark.parametrize(
    "headers, exception_message",
    [
        ({"NHSD-ID-Token": "P5.Cp.Cd"}, "Incorrect vot level"),
        ({"NHSD-ID-Token": "P9.Cp.Cd"}, "Incorrect vot level"),
        ({"NHSD-ID-Token": "Something random"}, "Incorrect vot level"),
        ({"NHSD-ID-Token": ""}, "Failed to retrieve vot level for logged in user"),
        ({}, "Failed to retrieve vot level for logged in user"),
    ],
)
def test_validate_vot_level_access_denied_exception(
    headers: dict, exception_message: str
) -> None:
    """Test the validate_vot_level func when invalid header."""
    # Arrange
    with app.test_request_context(headers=headers):
        # Act & Assert
        with pytest.raises(AccessDenied, match=exception_message):
            validate_vot_level()


def test_validate_ods_code() -> None:
    """Test the validate_ods_code func."""
    # Arrange
    with app.test_request_context(headers={"X-ODS-Code": "some od code"}):
        # Act & Assert
        validate_ods_code()


@pytest.mark.parametrize("headers", [{"X-ODS-Code": ""}, {}])
def test_validate_ods_code_access_denied_exception(headers: dict) -> None:
    """Test the validate_ods_code func when missing required header."""
    # Arrange
    with app.test_request_context(headers=headers):
        # Act & Assert
        with pytest.raises(MissingValue, match="Missing ods code"):
            validate_ods_code()


def test_validate_request_id() -> None:
    """Test the validate_request_id func."""
    # Arrange
    with app.test_request_context(headers={"X-Request-ID": str(uuid4())}):
        # Act & Assert
        validate_request_id()


@pytest.mark.parametrize(
    "headers, exception, exception_message",
    [
        ({"X-Request-ID": "some string"}, InvalidValue, "Invalid request id"),
        ({"X-Request-ID": ""}, MissingValue, "Missing request id"),
        ({}, MissingValue, "Missing request id"),
    ],
)
def test_validate_request_id_access_denied_exception(
    headers: dict, exception: ApiException, exception_message: str
) -> None:
    """Test the validate_request_id func when invalid required header."""
    # Arrange
    with app.test_request_context(headers=headers):
        # Act & Assert
        with pytest.raises(exception, match=exception_message):
            validate_request_id()


@pytest.mark.parametrize(
    "headers", [{"X-Correlation-ID": str(uuid4())}, {"X-Correlation-ID": ""}, {}]
)
def test_validate_correlation_id(headers: dict) -> None:
    """Test the validate_correlation_id func."""
    # Arrange
    with app.test_request_context(headers=headers):
        # Act & Assert
        validate_correlation_id()


def test_validate_correlation_id_access_denied_exception() -> None:
    """Test the validate_correlation_id func when invalid header."""
    # Arrange
    with app.test_request_context(headers={"X-Correlation-ID": "some string"}):
        # Act & Assert
        with pytest.raises(InvalidValue, match="Invalid correlation id"):
            validate_correlation_id()


def test_validate_forward_to() -> None:
    """Test the validate_forward_to func."""
    # Arrange
    with app.test_request_context(headers={"X-Forward-To": "https://example.com"}):
        # Act & Assert
        validate_forward_to()


@pytest.mark.parametrize(
    "headers, exception, exception_message",
    [
        ({"X-Forward-To": "some string"}, InvalidValue, "Invalid forward to"),
        ({"X-Forward-To": ""}, MissingValue, "Missing forward to"),
        ({}, MissingValue, "Missing forward to"),
    ],
)
def test_validate_forward_to_access_denied_exception(
    headers: dict, exception: ApiException, exception_message: str
) -> None:
    """Test the validate_forward_to func when invalid required header."""
    # Arrange
    with app.test_request_context(headers=headers):
        # Act & Assert
        with pytest.raises(exception, match=exception_message):
            validate_forward_to()

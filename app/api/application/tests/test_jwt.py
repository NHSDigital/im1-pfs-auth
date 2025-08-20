import pytest
from jwt import encode

from app.api.application.jwt import get_nhs_number_from_jwt_token
from app.api.domain.exception import AccessDeniedError


@pytest.mark.parametrize("vot_level", ["P9.Cp.Cd", "P9.Cp.Ck", "P9.Cm"])
def test_get_nhs_number_from_jwt_token(vot_level: str) -> None:
    """Test the get_nhs_number_from_jwt_token function."""
    # Arrange
    logged_in_user_token = encode(
        {
            "identity_proofing_level": "P9",
            "vot": vot_level,
            "nhs_number": "proxy nhs number",
        },
        key=None,
        algorithm="none",
    )
    token = encode(
        {"nhs_number": "patient nhs number", "act": {"sub": logged_in_user_token}},
        key=None,
        algorithm="none",
    )
    # Act
    actual_result = get_nhs_number_from_jwt_token(token)

    # Assert
    assert actual_result == ("patient nhs number", "proxy nhs number")


def test_get_nhs_number_from_jwt_token_missing_patient_nhs_number() -> None:
    """Test the get_nhs_number_from_jwt_token function when missing patient nhs number."""  # noqa: E501
    # Arrange
    logged_in_user_token = encode(
        {
            "identity_proofing_level": "P9",
            "vot": "P9.Cp.Cd",
            "nhs_number": "proxy nhs number",
        },
        key=None,
        algorithm="none",
    )
    token = encode(
        {"act": {"sub": logged_in_user_token}},
        key=None,
        algorithm="none",
    )
    # Act & Assert
    with pytest.raises(
        AccessDeniedError, match="Failed to retrieve nhs number from token"
    ):
        get_nhs_number_from_jwt_token(token)


def test_get_nhs_number_from_jwt_token_missing_proxy_nhs_number() -> None:
    """Test the get_nhs_number_from_jwt_token function when missing proxy nhs number."""
    # Arrange
    logged_in_user_token = encode(
        {
            "identity_proofing_level": "P9",
            "vot": "P9.Cp.Cd",
        },
        key=None,
        algorithm="none",
    )
    token = encode(
        {"nhs_number": "patient nhs number", "act": {"sub": logged_in_user_token}},
        key=None,
        algorithm="none",
    )
    # Act & Assert
    with pytest.raises(
        AccessDeniedError, match="Failed to retrieve nhs number from token"
    ):
        get_nhs_number_from_jwt_token(token)


@pytest.mark.parametrize("proofing_level", ["P5", "P0", "something random", "", None])
def test_get_nhs_number_from_jwt_token_invalid_proxy_proofing_level(
    proofing_level: str,
) -> None:
    """Test the get_nhs_number_from_jwt_token function when invalid proxy proofing level."""  # noqa: E501
    # Arrange
    logged_in_user_token = encode(
        {
            "identity_proofing_level": proofing_level,
            "vot": "P9.Cp.Cd",
            "nhs_number": "proxy nhs number",
        },
        key=None,
        algorithm="none",
    )
    token = encode(
        {"nhs_number": "patient nhs number", "act": {"sub": logged_in_user_token}},
        key=None,
        algorithm="none",
    )
    # Act & Assert
    with pytest.raises(
        AccessDeniedError, match="Logged in user is not P9 proofing level"
    ):
        get_nhs_number_from_jwt_token(token)


@pytest.mark.parametrize(
    "vot_level", ["P5.Cp.Cd", "P0.Cp.Cd", "something random", "", None]
)
def test_get_nhs_number_from_jwt_token_invalid_proxy_vot_level(vot_level: str) -> None:
    """Test the get_nhs_number_from_jwt_token function when invalid proxy proofing level."""  # noqa: E501
    # Arrange
    logged_in_user_token = encode(
        {
            "identity_proofing_level": "P9",
            "vot": vot_level,
            "nhs_number": "proxy nhs number",
        },
        key=None,
        algorithm="none",
    )
    token = encode(
        {"nhs_number": "patient nhs number", "act": {"sub": logged_in_user_token}},
        key=None,
        algorithm="none",
    )
    # Act & Assert
    with pytest.raises(
        AccessDeniedError, match="Logged in user has incorrect vot level"
    ):
        get_nhs_number_from_jwt_token(token)

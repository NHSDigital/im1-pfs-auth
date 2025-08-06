from flask import request
from uuid import UUID

from .exception import AccessDenied, InvalidValue, MissingValue


def validate_nhs_number() -> None:
    """Validates Logged in User's NHS Number from Request Header

    If unsuccessful will raise an AccessDenied Exception
    """
    logged_in_user_nhs_number = request.headers.get("NHSD-NHSlogin-NHS-Number")
    if not logged_in_user_nhs_number:
        raise AccessDenied("Failed to retrieve NHS Number for logged in user")


def validate_proofing_level() -> None:
    """Validates Logged in User's proofing level from Request Header

    If unsuccessful will raise an AccessDenied Exception
    """
    logged_in_user_proofing_level = request.headers.get(
        "NHSD-NHSlogin-Identity-Proofing-Level"
    )
    if not logged_in_user_proofing_level:
        raise AccessDenied("Failed to retrieve proofing level for logged in user")
    if logged_in_user_proofing_level not in ["P9"]:
        raise AccessDenied("Incorrect proofing level")


def validate_vot_level() -> None:
    """Validates Logged in User's vot level from Request Header

    If unsuccessful will raise an AccessDenied Exception
    """
    logged_in_user_id_token = request.headers.get("NHSD-ID-Token")
    if not logged_in_user_id_token:
        raise AccessDenied("Failed to retrieve vot level for logged in user")
    logged_in_user_vot_level = "P9.Cp.Cd"  # TODO: Will need to decode ID Token
    if logged_in_user_vot_level not in ["P9.Cp.Cd", "P9.Cp.Ck", "P9.Cm"]:
        raise AccessDenied("Incorrect vot level")


def validate_ods_code() -> None:
    """Validates ods code from Request Header

    If unsuccessful will raise a MissingValue Exception
    """
    ods_code = request.headers.get("X-ODS-Code")
    if not ods_code:
        raise MissingValue("Missing ods code")


def validate_request_id() -> None:
    """Validates request id from Request Header

    If unsuccessful will raise a MissingValue or InvalidValue Exception
    """
    request_id = request.headers.get("X-Request-ID")
    if not request_id:
        raise MissingValue("Missing request id")
    try:
        UUID(str(request_id))
    except ValueError:
        raise MissingValue("Invalid request id")


def validate_correlation_id() -> None:
    """Validates correlation id from Request Header

    If unsuccessful will raise an InvalidValue Exception
    """
    correlation_id = request.headers.get("X-Request-ID")
    try:
        UUID(str(correlation_id))
    except ValueError:
        raise InvalidValue("Invalid correlation id")


def validate_forward_to() -> None:
    """Validates forward to from Request Header

    If unsuccessful will raise a MissingValue or InvalidValue Exception
    """
    forward_to = request.headers.get("X-Forward-To")
    if not forward_to:
        raise MissingValue("Missing forward to")
    if not forward_to.startswith("https:"):
        raise InvalidValue("Invalid forward to")

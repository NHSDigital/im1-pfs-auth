from jwt import decode

from ..domain.exception import AccessDeniedError


def __fetch_nhs_number(decoded_token: dict) -> str:
    """Fetch patient NHS number from decoded jwt token.

    Args:
        decoded_token (str): Decoded JWT token

    Returns:
        str: NHS number
    """
    nhs_number = decoded_token.get("nhs_number")
    if not nhs_number:
        msg = "Failed to retrieve nhs number from token"
        raise AccessDeniedError(msg)

    return nhs_number


def __fetch_proxy_nhs_number(decoded_token: dict) -> str:
    """Fetch proxy NHS number from decoded jwt token.

    Args:
        decoded_token (str): Decoded JWT token

    Returns:
        str: NHS number
    """
    if decoded_token.get("identity_proofing_level") != "P9":
        msg = "Logged in user is not P9 proofing level"
        raise AccessDeniedError(msg)
    if decoded_token.get("vot") not in ["P9.Cp.Cd", "P9.Cp.Ck", "P9.Cm"]:
        msg = "Logged in user has incorrect vot level"
        raise AccessDeniedError(msg)

    return __fetch_nhs_number(decoded_token)


def get_nhs_number_from_jwt_token(jwt_token: str) -> tuple[str, str]:
    """Decodes JWT token and returns patient and proxy nhs numbers.

    Args:
        jwt_token (str): JWT composite token

    Returns:
        tuple[str, str]: Patient and proxy NHS numbers
    """
    decoded_token = decode(
        jwt_token,
        algorithms=["RS512"],
        options={"verify_signature": False},
    )
    patient_nhs_number = __fetch_nhs_number(decoded_token)

    proxy_decoded_token = decode(
        decoded_token.get("act", {}).get("sub"),
        algorithms=["RS512"],
        options={"verify_signature": False},
    )
    proxy_nhs_number = __fetch_proxy_nhs_number(proxy_decoded_token)

    return (patient_nhs_number, proxy_nhs_number)

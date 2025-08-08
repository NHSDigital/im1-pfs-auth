from jwt import decode
from ..domain.exception import AccessDenied


def __fetch_nhs_number(decoded_token: dict, is_logged_in_user: bool) -> str:
    """Fetch NHS number from decoded jwt token

    Args:
        decoded_token (str): Decoded JWT token
        is_logged_in_user (bool): Identifies if decoded jwt token is for the logged in user

    Returns:
        str: NHS number
    """
    if is_logged_in_user:
        if decoded_token.get("identity_proofing_level") != "P9":
            raise AccessDenied("Logged in user is not P9 proofing level")
        if decoded_token.get("vot") not in ["P9.Cp.Cd", "P9.Cp.Ck", "P9.Cm"]:
            raise AccessDenied("Logged in user has incorrect vot level")

    nhs_number = decoded_token.get("nhs_number")
    if not nhs_number:
        raise AccessDenied("Failed to retrieve nhs number from token")

    return nhs_number


def get_nhs_number_from_jwt_token(jwt_token: str):
    """Decodes JWT token and returns patient and proxy nhs numbers

    Args:
        token (str): JWT composite token

    Returns:
        tuple[str, str]: Patient and proxy NHS numbers
    """
    decoded_token = decode(
        jwt_token,
        algorithms=["RS512"],
        options={"verify_signature": False},
    )
    patient_nhs_number = __fetch_nhs_number(decoded_token, is_logged_in_user=False)

    proxy_decoded_token = decode(
        decoded_token.get("act", {}).get("sub"),
        algorithms=["RS512"],
        options={"verify_signature": False},
    )
    proxy_nhs_number = __fetch_nhs_number(proxy_decoded_token, is_logged_in_user=True)

    return (patient_nhs_number, proxy_nhs_number)

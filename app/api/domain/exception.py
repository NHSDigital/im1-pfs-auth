from http import HTTPStatus


class ApiError(Exception):
    """Base class for custom exceptions."""

    status_code: HTTPStatus
    message: str


class AccessDeniedError(ApiError):
    """Exception for when request is not authorised to access resource."""

    status_code = HTTPStatus.UNAUTHORIZED
    message = "Missing or invalid OAuth 2.0 bearer token in request."


class DownstreamError(ApiError):
    """Exception for when there is a downstream error."""

    status_code = HTTPStatus.BAD_GATEWAY
    message = "Downstream Service Error."


class InvalidValueError(ApiError):
    """Exception for when request contains a value that is invalid."""

    status_code = HTTPStatus.BAD_REQUEST
    message = "The request was unsuccessful due to invalid value."


class MissingValueError(ApiError):
    """Exception for when request is missing a required value."""

    status_code = HTTPStatus.BAD_REQUEST
    message = "The request was unsuccessful due to missing required value."

from http import HTTPStatus


class ApiException(Exception):
    """Base class for custom exceptions"""

    status_code: HTTPStatus
    message: str


class AccessDenied(ApiException):
    """Exception for when request is not authorised to access resource"""

    status_code = HTTPStatus.UNAUTHORIZED
    message = "Missing or invalid OAuth 2.0 bearer token in request."


class DownstreamError(ApiException):
    """Exception for when there is a downstream error"""

    status_code = HTTPStatus.BAD_GATEWAY
    message = "Downstream Service Error."


class InvalidValue(ApiException):
    """Exception for when request contains a value that is invalid"""

    status_code = HTTPStatus.BAD_REQUEST
    message = "The request was unsuccessful due to invalid value."


class MissingValue(ApiException):
    """Exception for when request is missing a required value"""

    status_code = HTTPStatus.BAD_REQUEST
    message = "The request was unsuccessful due to missing required value."

from http import HTTPStatus


class ApiError(Exception):
    """Base class for custom exceptions."""

    status_code: HTTPStatus
    message: dict


class AccessDeniedError(ApiError):
    """Exception for when bearer token is missing or malformed."""

    status_code = HTTPStatus.UNAUTHORIZED
    body = {  # noqa: RUF012
        "issue": [
            {
                "code": "forbidden",
                "details": {
                    "coding": [
                        {
                            "code": "ACCESS_DENIED",
                            "display": "Missing or invalid OAuth 2.0 bearer token in request",  # noqa: E501
                            "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                            "version": "1",
                        }
                    ]
                },
                "diagnostics": "Missing or invalid OAuth 2.0 bearer token in request",
                "severity": "error",
            }
        ],
        "resourceType": "OperationOutcome",
    }


class ForbiddenError(ApiError):
    """Exception for when user is not authorised to access resource."""

    status_code = HTTPStatus.FORBIDDEN
    body = {  # noqa: RUF012
        "issue": [
            {
                "code": "forbidden",
                "details": {
                    "coding": [
                        {
                            "code": "ACCESS_DENIED",
                            "display": "User does not have access to online services",
                            "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                            "version": "1",
                        }
                    ]
                },
                "diagnostics": "User does not have access to online services",
                "severity": "error",
            }
        ],
        "resourceType": "OperationOutcome",
    }


class NotFoundError(ApiError):
    """Exception for when user does not have an online account with supplier."""

    status_code = HTTPStatus.NOT_FOUND
    body = {  # noqa: RUF012
        "issue": [
            {
                "code": "exception",
                "details": {
                    "coding": [
                        {
                            "code": "RESOURCE_NOT_FOUND",
                            "display": "Resource not found",
                            "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                            "version": "1",
                        }
                    ]
                },
                "diagnostics": "User does not have an online account",
                "severity": "error",
            }
        ],
        "resourceType": "OperationOutcome",
    }


class DownstreamError(ApiError):
    """Exception for when there is a downstream error."""

    status_code = HTTPStatus.BAD_GATEWAY
    body = {  # noqa: RUF012
        "issue": [
            {
                "code": "processing",
                "details": {
                    "coding": [
                        {
                            "code": "DOWNSTREAM_SERVICE_ERROR",
                            "display": "Failed to generate response",
                            "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                            "version": "1",
                        }
                    ]
                },
                "diagnostics": "Downstream Service Error - Failed to generate response is present in the response",  # noqa: E501
                "severity": "error",
            }
        ],
        "resourceType": "OperationOutcome",
    }


class InvalidValueError(ApiError):
    """Exception for when request contains a value that is invalid."""

    status_code = HTTPStatus.BAD_REQUEST
    body = {  # noqa: RUF012
        "issue": [
            {
                "code": "exception",
                "details": {
                    "coding": [
                        {
                            "code": "INVALID_HEADER",
                            "display": "A header is invalid",
                            "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                            "version": "1",
                        }
                    ]
                },
                "diagnostics": "Invalid header request",
                "severity": "error",
            }
        ],
        "resourceType": "OperationOutcome",
    }


class MissingValueError(ApiError):
    """Exception for when request is missing a required value."""

    status_code = HTTPStatus.BAD_REQUEST
    body = {  # noqa: RUF012
        "issue": [
            {
                "code": "exception",
                "details": {
                    "coding": [
                        {
                            "code": "MISSING_HEADER",
                            "display": "A required header is missing",
                            "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                            "version": "1",
                        }
                    ]
                },
                "diagnostics": "The request was unsuccessful due to missing required value",  # noqa: E501
                "severity": "error",
            }
        ],
        "resourceType": "OperationOutcome",
    }


class InternalServierError(ApiError):
    """Generic Exception."""

    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    body = {  # noqa: RUF012
        "issue": [
            {
                "code": "exception",
                "details": {
                    "coding": [
                        {
                            "code": "SERVER_ERROR",
                            "display": "Failed to generate response",
                            "system": "https://fhir.nhs.uk/R4/CodeSystem/IM1-PFS-Auth-ErrorOrWarningCode",
                            "version": "1",
                        }
                    ]
                },
                "diagnostics": "Internal Server Error - Failed to generate response is present in the response",  # noqa: E501
                "severity": "error",
            }
        ],
        "resourceType": "OperationOutcome",
    }

from pydantic import BaseModel, field_validator

from .exception import (
    AccessDenied,
    InvalidValue,
    MissingValue,
)


class ForwardRequest(BaseModel):
    """A domain-level data model that encapsulates all the essential information needed to forward a client’s request to an external backend system"""

    application_id: str
    forward_to: str
    patient_nhs_number: str
    patient_ods_code: str
    proxy_nhs_number: str

    @field_validator("application_id", "patient_ods_code", "forward_to")
    def validate_required_value(cls, v) -> None:
        """Validates if required value is present

        If unsuccessful will raise a MissingValue Exception
        """
        if not v:
            raise MissingValue("Missing required value")

    @field_validator("patient_nhs_number", "proxy_nhs_number")
    def validate_nhs_number(cls, v) -> None:
        """Validates nhs number

        If unsuccessful will raise an AccessDenied Exception
        """
        if not v:
            raise AccessDenied("Failed to retrieve NHS Number")

    @field_validator("forward_to")
    def validate_url(cls, v):
        """Validates url

        If unsuccessful will raise An InvalidValue Exception
        """
        if not v.startswith("https:"):
            raise InvalidValue("Invalid url")

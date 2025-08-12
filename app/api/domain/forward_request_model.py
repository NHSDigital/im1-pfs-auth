from pydantic import BaseModel, field_validator, model_validator

from .exception import (
    AccessDeniedError,
    InvalidValueError,
    MissingValueError,
)


class ForwardRequest(BaseModel):
    """A domain-level data model that encapsulates all the essential information needed to forward a clients request to an external backend system."""

    application_id: str
    forward_to: str
    patient_nhs_number: str
    patient_ods_code: str
    proxy_nhs_number: str

    @model_validator(mode="before")
    def validate_required_value(cls, values: list) -> list:
        """Validates if required value is present.

        If unsuccessful will raise a MissingValueError Exception
        """
        required_fields = ["application_id", "patient_ods_code", "forward_to"]
        for required_field in required_fields:
            if required_field not in values or not values[required_field]:
                msg = "Missing required value"
                raise MissingValueError(msg)
        return values

    @model_validator(mode="before")
    def validate_string(cls, values: list) -> list:
        """Validates if value is a string.

        If unsuccessful will raise a MissingValueError Exception
        """
        string_fields = ["application_id", "patient_ods_code", "forward_to"]
        for string_field in string_fields:
            if not isinstance(string_field, str):
                msg = "Invalid value"
                raise InvalidValueError(msg)
        return values

    @model_validator(mode="before")
    def validate_nhs_number(cls, values: list) -> list:
        """Validates nhs number.

        If unsuccessful will raise an AccessDeniedError Exception
        """
        nhs_number_fields = ["patient_nhs_number", "proxy_nhs_number"]
        for nhs_number_field in nhs_number_fields:
            rules = [
                nhs_number_field in values,
                values[nhs_number_field],
                isinstance(values[nhs_number_field], str)
                and len(values[nhs_number_field]) == 10,
                isinstance(values[nhs_number_field], str)
                and values[nhs_number_field].isnumeric(),
            ]

            if not all(rules):
                msg = "Failed to retrieve NHS Number"
                raise AccessDeniedError(msg)
        return values

    @field_validator("forward_to")
    def validate_url(cls, value: str) -> str:
        """Validates url.

        If unsuccessful will raise An InvalidValueError Exception
        """
        if not value.startswith("https:"):
            msg = "Invalid url"
            raise InvalidValueError(msg)

        return value

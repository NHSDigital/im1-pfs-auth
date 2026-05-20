from pydantic import BaseModel, ConfigDict, SerializeAsAny, field_validator
from pydantic.alias_generators import to_camel


class Permissions(BaseModel):
    """A data model that encapsulates all the essential permissions data."""


class Demographics(BaseModel):
    """A data model that encapsulates all the essential demographic data."""

    model_config = ConfigDict(alias_generator=to_camel)

    first_name: str
    surname: str
    title: str
    date_of_birth: str
    permissions: Permissions


class ForwardResponse(BaseModel):
    """All the essential information needed to forward a external backend system response to the client."""  # noqa: E501

    model_config = ConfigDict(alias_generator=to_camel)

    session_id: str
    supplier: str
    ods_code: str
    user: SerializeAsAny[Demographics]
    patients: list[SerializeAsAny[Demographics]]

    @field_validator("patients")
    def patients_must_not_be_empty(cls, v: list) -> list:  # noqa: N805
        """Check if patient array is empty."""
        if not v:
            error_msg = "patients cannot be empty"
            raise ValueError(error_msg)
        return v

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel


class Demographics(BaseModel):
    """A data model that encapsulates all the essential demographic data."""

    model_config = ConfigDict(alias_generator=to_camel)

    first_name: str
    surname: str
    title: str


class ForwardResponse(BaseModel):
    """All the essential information needed to forward a external backend system response to the client."""  # noqa: E501

    model_config = ConfigDict(alias_generator=to_camel)

    session_id: str
    supplier: str
    proxy: Demographics
    patients: list[Demographics]

    @field_validator("patients")
    def patients_must_not_be_empty(cls, v: list) -> list:  # noqa: N805
        """Check if patient array is empty."""
        if not v:
            error_msg = "patients cannot be empty"
            raise ValueError(error_msg)
        return v

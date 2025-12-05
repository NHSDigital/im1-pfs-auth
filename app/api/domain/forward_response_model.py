from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.alias_generators import to_camel


class Demographics(BaseModel):
    """A data model that encapsulates all the essential demographic data."""

    model_config = ConfigDict(alias_generator=to_camel)

    first_name: str
    surname: str
    title: str


class ViewPermissions(BaseModel):
    """All the view permissions data the proxy holds for a patient."""

    model_config = ConfigDict(alias_generator=to_camel)

    medical_record: bool
    summary_medical_record: bool
    allergies_medical_record: bool
    consultations_medical_record: bool
    immunisations_medical_record: bool
    documents_medical_record: bool
    medication_medical_record: bool
    problems_medical_record: bool
    test_results_medical_record: bool
    record_audit: bool
    record_sharing: bool


class Permissions(BaseModel):
    """All the permissions data a proxy holds for a patient."""

    model_config = ConfigDict(alias_generator=to_camel)

    access_system_connect: bool  # tpp only
    book_appointments: bool
    change_pharmacy: bool
    message_practice: bool
    provide_information_to_practice: bool
    request_medication: bool
    update_demographics: bool  # emis only
    manage_online_triage: bool
    view: ViewPermissions


class Patient(Demographics):
    """Patient data model that extends Demographics with the addition of permissions."""

    permissions: Permissions


class ForwardResponse(BaseModel):
    """All the essential information needed to forward a external backend system response to the client."""  # noqa: E501

    model_config = ConfigDict(alias_generator=to_camel)

    session_id: str
    supplier: str
    proxy: Demographics
    patients: list[Patient]

    @field_validator("patients")
    def patients_must_not_be_empty(cls, v: list[Patient]) -> list[Patient]:  # noqa: N805
        """Check if patient array is empty."""
        if not v:
            error_msg = "patients cannot be empty"
            raise ValueError(error_msg)
        return v
